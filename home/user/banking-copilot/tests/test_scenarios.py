#!/usr/bin/env python3
"""
End-to-End Test Suite for Banking Copilot Actions & Mock Core Banking Backend
"""

import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_test(name, fn):
    print(f"[*] Running: {name} ... ", end="")
    try:
        fn()
        print("✅ PASSED")
        return True
    except Exception as e:
        print(f"❌ FAILED ({e})")
        return False

def http_get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode())

def http_post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f"{BASE_URL}{path}", data=data, headers={"Content-Type": "application/json", "Accept": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode())

def test_health():
    code, data = http_get("/health")
    assert code == 200
    assert data["status"] == "ONLINE"

def test_get_customer_accounts():
    code, data = http_get("/api/v1/customers/CUST-10029/accounts")
    assert code == 200
    assert data["customerName"] == "Alex Morgan"
    assert len(data["accounts"]) == 2

def test_get_account_balance():
    code, data = http_get("/api/v1/accounts/ACC-CHK-9812/balance")
    assert code == 200
    assert data["availableBalance"] == 4520.50
    assert data["currency"] == "USD"

def test_get_transactions():
    code, data = http_get("/api/v1/accounts/ACC-CHK-9812/transactions?limit=3")
    assert code == 200
    assert len(data["transactions"]) == 3
    assert data["transactions"][0]["merchant"] == "Whole Foods Market #102"

def test_otp_step_up_flow():
    # 1. Dispatch OTP
    code, data = http_post("/api/v1/auth/otp/send", {"customerId": "CUST-10029", "actionType": "CARD_UNFREEZE"})
    assert code == 200
    chal_id = data["challengeId"]
    assert chal_id.startswith("CHAL-")

    # 2. Verify OTP with valid sandbox code
    code, vdata = http_post("/api/v1/auth/otp/verify", {"challengeId": chal_id, "otpCode": "123456"})
    assert code == 200
    assert vdata["verified"] is True
    assert vdata["verificationToken"].startswith("VTOK-")

def test_card_freeze():
    code, data = http_post("/api/v1/cards/CARD-VISA-7711/status", {
        "newStatus": "FROZEN",
        "reason": "Customer misplaced card in transit"
    })
    assert code == 200
    assert data["status"] == "FROZEN"
    assert data["confirmationCode"].startswith("CONF-")

def test_create_dispute():
    code, data = http_post("/api/v1/disputes/create", {
        "customerId": "CUST-10029",
        "accountId": "ACC-CHK-9812",
        "transactionId": "TXN-9010",
        "disputeReason": "UNRECOGNIZED_MERCHANT",
        "customerRemarks": "Did not authorize online purchase from UK retailer."
    })
    assert code == 201
    assert data["status"] == "UNDER_REVIEW"
    assert data["provisionalCreditEligible"] is True
    assert data["disputeCaseId"].startswith("DSP-")

if __name__ == "__main__":
    print("==================================================")
    print(" Banking Copilot Studio API & Action Test Suite   ")
    print("==================================================")
    tests = [
        ("API Gateway Health Check", test_health),
        ("Customer Accounts Retrieval", test_get_customer_accounts),
        ("Real-time Balance Check", test_get_account_balance),
        ("Recent Transactions Lookup", test_get_transactions),
        ("Two-Factor Step-Up OTP Verification", test_otp_step_up_flow),
        ("Autonomous Card Freeze Execution", test_card_freeze),
        ("Transaction Dispute Filing", test_create_dispute),
    ]

    passed = 0
    for name, fn in tests:
        if run_test(name, fn):
            passed += 1

    print("==================================================")
    print(f"Test Summary: {passed}/{len(tests)} passed.")
    print("==================================================")
    if passed != len(tests):
        sys.exit(1)
