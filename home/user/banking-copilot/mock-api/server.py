#!/usr/bin/env python3
"""
Mock Core Banking Service API for Microsoft Copilot Studio Integration Testing
Runs a local REST API matching the OpenAPI 3.0 specification.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
import urllib.parse
from datetime import datetime, timezone
import random

# In-memory mock database
MOCK_DB = {
    "customers": {
        "CUST-10029": {
            "customerId": "CUST-10029",
            "customerName": "Alex Morgan",
            "email": "alex.morgan@example.com",
            "phone": "+1 (555) 019-8812",
            "accounts": [
                {
                    "accountId": "ACC-CHK-9812",
                    "accountType": "CHECKING",
                    "accountNumberMasked": "******9812",
                    "currency": "USD",
                    "availableBalance": 4520.50,
                    "currentLedgerBalance": 4650.00,
                    "status": "ACTIVE"
                },
                {
                    "accountId": "ACC-SAV-4109",
                    "accountType": "SAVINGS",
                    "accountNumberMasked": "******4109",
                    "currency": "USD",
                    "availableBalance": 28450.00,
                    "currentLedgerBalance": 28450.00,
                    "status": "ACTIVE"
                }
            ],
            "cards": [
                {
                    "cardId": "CARD-VISA-7711",
                    "cardMasked": "Visa Platinum ending in 7711",
                    "status": "ACTIVE",
                    "linkedAccountId": "ACC-CHK-9812",
                    "updatedAt": "2026-09-01T10:00:00Z"
                }
            ]
        }
    },
    "transactions": {
        "ACC-CHK-9812": [
            {
                "transactionId": "TXN-9012",
                "postedDate": "2026-09-29",
                "merchant": "Whole Foods Market #102",
                "category": "Groceries",
                "amount": -84.32,
                "currency": "USD",
                "status": "POSTED"
            },
            {
                "transactionId": "TXN-9011",
                "postedDate": "2026-09-28",
                "merchant": "Uber Technologies Inc",
                "category": "Transport",
                "amount": -24.50,
                "currency": "USD",
                "status": "POSTED"
            },
            {
                "transactionId": "TXN-9010",
                "postedDate": "2026-09-27",
                "merchant": "Unknown Online Retailer - London UK",
                "category": "E-Commerce",
                "amount": -329.99,
                "currency": "USD",
                "status": "POSTED"
            },
            {
                "transactionId": "TXN-9009",
                "postedDate": "2026-09-26",
                "merchant": "Payroll Direct Deposit - ACME Corp",
                "category": "Income",
                "amount": 3200.00,
                "currency": "USD",
                "status": "POSTED"
            }
        ]
    },
    "active_challenges": {},
    "disputes": []
}

class BankingApiHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-api-key')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-api-key')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Health check
        if path == "/health" or path == "/":
            self._send_json(200, {"status": "ONLINE", "service": "Banking Core API Mock", "version": "1.0.0"})
            return

        # /api/v1/customers/{customerId}/accounts
        cust_match = re.match(r"^/api/v1/customers/([^/]+)/accounts$", path)
        if cust_match:
            cust_id = cust_match.group(1)
            customer = MOCK_DB["customers"].get(cust_id)
            if customer:
                self._send_json(200, {
                    "customerId": customer["customerId"],
                    "customerName": customer["customerName"],
                    "accounts": customer["accounts"]
                })
            else:
                self._send_json(404, {"error": "CustomerNotFound", "message": f"Customer {cust_id} not found."})
            return

        # /api/v1/accounts/{accountId}/balance
        bal_match = re.match(r"^/api/v1/accounts/([^/]+)/balance$", path)
        if bal_match:
            acc_id = bal_match.group(1)
            for cust in MOCK_DB["customers"].values():
                for acc in cust["accounts"]:
                    if acc["accountId"] == acc_id:
                        self._send_json(200, {
                            "accountId": acc["accountId"],
                            "accountType": acc["accountType"],
                            "accountNumberMasked": acc["accountNumberMasked"],
                            "currency": acc["currency"],
                            "availableBalance": acc["availableBalance"],
                            "currentLedgerBalance": acc["currentLedgerBalance"],
                            "lastUpdated": datetime.now(timezone.utc).isoformat()
                        })
                        return
            self._send_json(404, {"error": "AccountNotFound", "message": f"Account {acc_id} not found."})
            return

        # /api/v1/accounts/{accountId}/transactions
        txn_match = re.match(r"^/api/v1/accounts/([^/]+)/transactions$", path)
        if txn_match:
            acc_id = txn_match.group(1)
            limit = int(query.get("limit", [5])[0])
            txns = MOCK_DB["transactions"].get(acc_id, [])[:limit]
            self._send_json(200, {
                "accountId": acc_id,
                "transactions": txns
            })
            return

        self._send_json(404, {"error": "NotFound", "message": f"Path {path} not recognized."})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length).decode('utf-8')) if length > 0 else {}

        # /api/v1/cards/{cardId}/status
        card_match = re.match(r"^/api/v1/cards/([^/]+)/status$", path)
        if card_match:
            card_id = card_match.group(1)
            new_status = body.get("newStatus", "FROZEN")
            reason = body.get("reason", "Customer request")
            
            # Locate card
            found_card = None
            for cust in MOCK_DB["customers"].values():
                for card in cust["cards"]:
                    if card["cardId"] == card_id:
                        card["status"] = new_status
                        card["updatedAt"] = datetime.now(timezone.utc).isoformat()
                        found_card = card
                        break

            if found_card:
                ref_code = f"CONF-{random.randint(1000, 9999)}-{new_status[:3]}"
                self._send_json(200, {
                    "cardId": found_card["cardId"],
                    "cardMasked": found_card["cardMasked"],
                    "status": found_card["status"],
                    "updatedAt": found_card["updatedAt"],
                    "confirmationCode": ref_code,
                    "reason": reason
                })
            else:
                self._send_json(404, {"error": "CardNotFound", "message": f"Card {card_id} not found."})
            return

        # /api/v1/disputes/create
        if path == "/api/v1/disputes/create":
            case_id = f"DSP-{datetime.now().year}-{random.randint(10000, 99999)}"
            dispute_record = {
                "disputeCaseId": case_id,
                "customerId": body.get("customerId"),
                "accountId": body.get("accountId"),
                "transactionId": body.get("transactionId"),
                "disputeReason": body.get("disputeReason"),
                "customerRemarks": body.get("customerRemarks", ""),
                "status": "UNDER_REVIEW",
                "provisionalCreditEligible": True,
                "estimatedResolutionDays": 10,
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
            MOCK_DB["disputes"].append(dispute_record)
            self._send_json(201, {
                "disputeCaseId": case_id,
                "status": "UNDER_REVIEW",
                "provisionalCreditEligible": True,
                "estimatedResolutionDays": 10,
                "message": f"Dispute case {case_id} registered. Our fraud & compliance specialists will review within 24-48 hours."
            })
            return

        # /api/v1/auth/otp/send
        if path == "/api/v1/auth/otp/send":
            cust_id = body.get("customerId", "CUST-10029")
            challenge_id = f"CHAL-{random.randint(100000, 999999)}"
            MOCK_DB["active_challenges"][challenge_id] = {
                "customerId": cust_id,
                "code": "123456",  # fixed for mock testing
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
            self._send_json(200, {
                "challengeId": challenge_id,
                "maskedDestination": "+1 (***) ***-8812",
                "expiresInSeconds": 300,
                "note": "For testing purposes in sandbox, pass '123456' as the OTP code."
            })
            return

        # /api/v1/auth/otp/verify
        if path == "/api/v1/auth/otp/verify":
            chal_id = body.get("challengeId")
            code = body.get("otpCode")
            challenge = MOCK_DB["active_challenges"].get(chal_id)
            if challenge and (code == "123456" or code == challenge.get("code")):
                self._send_json(200, {
                    "verified": True,
                    "verificationToken": f"VTOK-{random.randint(100000, 999999)}-VALID",
                    "message": "Step-up authentication succeeded."
                })
            else:
                self._send_json(400, {
                    "verified": False,
                    "verificationToken": None,
                    "message": "Invalid passcode or challenge expired. Try '123456' for sandbox testing."
                })
            return

        self._send_json(404, {"error": "NotFound", "message": f"Post endpoint {path} not recognized."})

if __name__ == "__main__":
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, BankingApiHandler)
    print("Mock Core Banking Server running on http://0.0.0.0:8000")
    httpd.serve_forever()
