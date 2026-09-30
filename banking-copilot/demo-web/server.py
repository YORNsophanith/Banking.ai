#!/usr/bin/env python3
"""
KEY Bank — Enterprise Agentic AI Banking System
Multi-Role Authentication & Management Server
Administrator: Mr. Sophanith Yorn
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone
import random

PORT = int(os.environ.get("PORT", 3000))
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
KB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge-base")

# Pre-configured Users & Roles Directory
USERS_DB = {
    "sophanith": {
        "id": "USR-ADMIN-001",
        "username": "sophanith",
        "name": "Mr. Sophanith Yorn",
        "nameKh": "លោក យន សុផានីត",
        "role": "Administrator",
        "roleKh": "អគ្គនាយកគ្រប់គ្រងប្រព័ន្ធ (Administrator)",
        "department": "Executive Board",
        "email": "sophanith.yorn@keybank.com",
        "avatar": "SY",
        "avatarBg": "linear-gradient(135deg, #1e40af 0%, #1e1b4b 100%)",
        "accessLevel": "SUPER_ADMIN",
        "badgeColor": "#3b82f6"
    },
    "ravith": {
        "id": "USR-FIN-002",
        "username": "ravith",
        "name": "Vn. Voeun Ravith",
        "nameKh": "វ.ន វឿន រ៉ាវិទ",
        "role": "Finance Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងហិរញ្ញវត្ថុ (Finance Manager)",
        "department": "Finance & Treasury",
        "email": "ravith.voeun@keybank.com",
        "avatar": "VR",
        "avatarBg": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
        "accessLevel": "FINANCE_ADMIN",
        "badgeColor": "#10b981"
    },
    "phirek": {
        "id": "USR-MKT-003",
        "username": "phirek",
        "name": "Vn. Hon Phirek",
        "nameKh": "វ.ន ហន ភិរ៉េក",
        "role": "Marketing Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងទីផ្សារ (Marketing Manager)",
        "department": "Growth & Marketing",
        "email": "phirek.hon@keybank.com",
        "avatar": "HP",
        "avatarBg": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
        "accessLevel": "MARKETING_ADMIN",
        "badgeColor": "#f59e0b"
    },
    "sokny": {
        "id": "USR-IT-004",
        "username": "sokny",
        "name": "Mr. San Sokny",
        "nameKh": "លោក សាន សុកនី",
        "role": "IT Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងបច្ចេកវិទ្យា (IT Manager)",
        "department": "Information Technology & Security",
        "email": "sokny.san@keybank.com",
        "avatar": "SS",
        "avatarBg": "linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%)",
        "accessLevel": "IT_ADMIN",
        "badgeColor": "#8b5cf6"
    },
    "vathanakboth": {
        "id": "USR-SALES-005",
        "username": "vathanakboth",
        "name": "Mr. Ly Vathanakboth",
        "nameKh": "លោក លី វឌ្ឍនៈបថ",
        "role": "Sale Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងផ្នែកលក់ (Sale Manager)",
        "department": "Retail & Corporate Sales",
        "email": "vathanakboth.ly@keybank.com",
        "avatar": "LV",
        "avatarBg": "linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%)",
        "accessLevel": "SALES_ADMIN",
        "badgeColor": "#0ea5e9"
    },
    "panha_n": {
        "id": "USR-SALES-006",
        "username": "panha_n",
        "name": "Mr. Noeun Panha",
        "nameKh": "លោក នឿន បញ្ញា",
        "role": "Sale Officer",
        "roleKh": "មន្ត្រីផ្នែកលក់ (Sale Officer)",
        "department": "Retail Sales",
        "email": "panha.noeun@keybank.com",
        "avatar": "NP",
        "avatarBg": "linear-gradient(135deg, #0d9488 0%, #134e4a 100%)",
        "accessLevel": "SALES_OFFICER",
        "badgeColor": "#14b8a6"
    },
    "panha_c": {
        "id": "USR-HR-007",
        "username": "panha_c",
        "name": "Ms. Chea Panha",
        "nameKh": "កញ្ញា ជា បញ្ញា",
        "role": "HR Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងធនធានមនុស្ស (HR Manager)",
        "department": "Human Resources",
        "email": "panha.chea@keybank.com",
        "avatar": "CP",
        "avatarBg": "linear-gradient(135deg, #db2777 0%, #831843 100%)",
        "accessLevel": "HR_ADMIN",
        "badgeColor": "#ec4899"
    },
    "nisa": {
        "id": "USR-MKT-008",
        "username": "nisa",
        "name": "Ms. Na Nisa",
        "nameKh": "កញ្ញា ណា នីសា",
        "role": "Marketing Officer",
        "roleKh": "មន្ត្រីផ្នែកទីផ្សារ (Marketing Officer)",
        "department": "Growth & Marketing",
        "email": "nisa.na@keybank.com",
        "avatar": "NN",
        "avatarBg": "linear-gradient(135deg, #ea580c 0%, #7c2d12 100%)",
        "accessLevel": "MARKETING_OFFICER",
        "badgeColor": "#f97316"
    },
    "customer": {
        "id": "CUST-10029",
        "username": "customer",
        "name": "Alex Morgan",
        "nameKh": "Alex Morgan (អតិថិជន)",
        "role": "Retail Customer",
        "roleKh": "អតិថិជនកម្រិតផ្លាទីនៀម (Platinum Customer)",
        "department": "Retail Banking",
        "email": "alex.morgan@example.com",
        "avatar": "AM",
        "avatarBg": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
        "accessLevel": "CUSTOMER",
        "badgeColor": "#3b82f6"
    }
}

# Live Banking State
STATE = {
    "activeUser": USERS_DB["sophanith"],
    "accounts": [
        {
            "accountId": "ACC-CHK-9812",
            "accountType": "Everyday Checking",
            "accountTypeKh": "គណនីចរន្តទូទៅ",
            "accountNumberMasked": "******9812",
            "currency": "$",
            "availableBalance": 4520.50,
            "currentLedgerBalance": 4650.00,
            "status": "Active",
            "statusKh": "សកម្ម"
        },
        {
            "accountId": "ACC-SAV-4109",
            "accountType": "High-Yield Savings (4.75% APY)",
            "accountTypeKh": "គណនីសន្សំការប្រាក់ខ្ពស់ (4.75% APY)",
            "accountNumberMasked": "******4109",
            "currency": "$",
            "availableBalance": 28450.00,
            "currentLedgerBalance": 28450.00,
            "status": "Active",
            "statusKh": "សកម្ម"
        }
    ],
    "cards": [
        {
            "cardId": "CARD-VISA-7711",
            "cardMasked": "Visa Platinum (•••• 7711)",
            "status": "ACTIVE",
            "statusKh": "សកម្ម (ACTIVE)",
            "expiry": "08/29",
            "linkedAccountId": "ACC-CHK-9812",
            "travelNotice": None
        }
    ],
    "transactions": [
        {
            "transactionId": "TXN-9012",
            "postedDate": "Today",
            "postedDateKh": "ថ្ងៃនេះ",
            "merchant": "Whole Foods Market #102",
            "category": "Groceries",
            "categoryKh": "ទិញទំនិញ / ម្ហូបអាហារ",
            "amount": -84.32,
            "status": "POSTED"
        },
        {
            "transactionId": "TXN-9011",
            "postedDate": "Yesterday",
            "postedDateKh": "ម្សិលមិញ",
            "merchant": "Uber Technologies Inc",
            "category": "Transport",
            "categoryKh": "ការធ្វើដំណើរ / ដឹកជញ្ជូន",
            "amount": -24.50,
            "status": "POSTED"
        },
        {
            "transactionId": "TXN-9010",
            "postedDate": "2 days ago",
            "postedDateKh": "២ ថ្ងៃមុន",
            "merchant": "Unknown Online Retailer - London UK",
            "category": "E-Commerce / Cross-Border",
            "categoryKh": "ទិញទំនិញអនឡាញ / ក្រៅប្រទេស",
            "amount": -329.99,
            "status": "POSTED"
        },
        {
            "transactionId": "TXN-9009",
            "postedDate": "Sep 26, 2026",
            "postedDateKh": "២៦ កញ្ញា ២០២៦",
            "merchant": "Direct Deposit - KEY Payroll Disburse",
            "category": "Income",
            "categoryKh": "ប្រាក់បៀវត្សរ៍ប្រចាំខែ",
            "amount": 3200.00,
            "status": "POSTED"
        }
    ],
    "disputes": [],
    "active_otp_challenges": {},
    "pending_actions": {}
}

def is_khmer_text(text):
    return bool(re.search(r'[\u1780-\u17FF]', text))

def execute_agentic_reasoning(user_text, session_id, lang_preference="auto", current_user=None):
    text = user_text.lower().strip()
    is_kh = is_khmer_text(user_text) or lang_preference == "km"
    user = current_user or STATE["activeUser"]
    user_name = user.get("nameKh") if is_kh else user.get("name")
    user_role = user.get("roleKh") if is_kh else user.get("role")
    
    logs = []
    response_payload = {
        "reply": "",
        "thoughtProcess": [],
        "toolCalls": [],
        "card": None,
        "suggestedActions": []
    }

    if is_kh:
        logs.append(f"🧠 ជំហានទី១ [KEY Bank AI Intent]: ទទួលសារពី {user_name} ({user_role}): '{user_text}'")
    else:
        logs.append(f"🧠 Step 1 [KEY Bank AI Intent]: User context {user['name']} ({user['role']}): '{user_text}'")

    if "123456" in text or re.search(r"\b\d{6}\b", text):
        otp_match = re.search(r"\b\d{6}\b", text).group(0)
        logs.append(f"🔧 Step 2 [Tool Call]: verifyStepUpOtp(challengeId='active', otpCode='{otp_match}')")
        
        if otp_match == "123456":
            logs.append("✅ Step 3 [Tool Result]: Step-up authentication SUCCESS.")
            pending = STATE["pending_actions"].get(session_id)
            if pending and pending.get("type") == "UNFREEZE":
                STATE["cards"][0]["status"] = "ACTIVE"
                STATE["cards"][0]["statusKh"] = "សកម្ម (ACTIVE)"
                logs.append("🔧 Step 4 [Tool Call]: updateCardStatus(cardId='CARD-VISA-7711', newStatus='ACTIVE')")
                
                if is_kh:
                    response_payload["reply"] = f"✅ **ការផ្ទៀងផ្ទាត់ជោគជ័យ!** សូមគោរព {user_name} កាត Visa លេខចុងក្រោយ **7711** ត្រូវបាន **ដោះសោ (UNFROZEN)** រួចរាល់ហើយ។"
                else:
                    response_payload["reply"] = f"✅ **Identity Verified!** {user['name']}, your KEY Bank Visa card ending in **7711** has been successfully **UNFROZEN**."
            else:
                if is_kh:
                    response_payload["reply"] = f"✅ **ការផ្ទៀងផ្ទាត់បានជោគជ័យ!** សូមជម្រាបសួរ {user_name} ({user_role}) តើខ្ញុំអាចជួយអ្វីបន្ថែម?"
                else:
                    response_payload["reply"] = f"✅ **Identity Verified!** Welcome {user['name']} ({user['role']}). How can I assist you with KEY Bank services today?"
        else:
            logs.append("❌ Step 3 [Tool Result]: Step-up authentication FAILED (Invalid OTP).")
            response_payload["reply"] = "⚠️ លេខកូដសម្ងាត់មិនត្រឹមត្រូវ។ សម្រាប់ demo សូមវាយបញ្ចូល: **123456**。" if is_kh else "⚠️ Invalid passcode. For demo testing, please enter **123456**."
        
        response_payload["thoughtProcess"] = logs
        return response_payload

    # Default fallback greeting
    if is_kh:
        logs.append(f"🧠 Step 2 [Generative LLM]: Synthesizing response for {user_name}.")
        response_payload["reply"] = f"សូមគោរពជម្រាបសួរ **{user_name}** ({user_role})! ខ្ញុំជា **ភ្នាក់ងារ AI ស្វ័យប្រវត្តិនៃធនាគារ KEY Bank**។ ខ្ញុំអាចជួយលោកអ្នកលើ:\n\n• 💳 **ពិនិត្យសមតុល្យ និងរបាយការណ៍ហិរញ្ញវត្ថុ**\n• 🔍 **សាកសួរប្រតិបត្តិការ និងការតវ៉ាក្លែងបន្លំ**\n• 🔒 **ការគ្រប់គ្រងសុវត្ថិភាព និងបង្កកកាតភ្លាមៗ**\n• ✈️ **កំណត់ការជូនដំណឹងពេលធ្វើដំណើរទៅក្រៅប្រទេស**\n• 📄 **តារាងថ្លៃសេវាធនាគារ និងដែនកំណត់**\n\nតើខ្ញុំអាចជួយអ្វីដល់លោកអ្នកនៅថ្ងៃនេះ?"
    else:
        logs.append(f"🧠 Step 2 [Generative LLM]: Synthesizing response for {user['name']}.")
        response_payload["reply"] = f"Welcome **{user['name']}** ({user['role']})! I am your **KEY Bank AI Copilot**. How may I assist you with enterprise services today?"

    response_payload["suggestedActions"] = ["Check my balances", "Why was I charged $329 in London?", "Freeze my Visa card", "Set travel notice for Japan"]
    response_payload["thoughtProcess"] = logs
    return response_payload

class DemoAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/users":
            self._send_json(200, list(USERS_DB.values()))
            return
        if parsed.path == "/api/state":
            self._send_json(200, STATE)
            return
        if parsed.path == "/api/reset":
            STATE["cards"][0]["status"] = "ACTIVE"
            STATE["cards"][0]["statusKh"] = "សកម្ម (ACTIVE)"
            STATE["cards"][0]["travelNotice"] = None
            STATE["disputes"] = []
            self._send_json(200, {"message": "State reset successfully", "state": STATE})
            return
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length).decode('utf-8')) if length > 0 else {}

        if parsed.path == "/api/login":
            username = body.get("username", "sophanith")
            user = USERS_DB.get(username)
            if user:
                STATE["activeUser"] = user
                self._send_json(200, {"status": "SUCCESS", "user": user})
            else:
                self._send_json(401, {"status": "ERROR", "message": "User not found"})
            return

        if parsed.path == "/api/register":
            name = body.get("name", "New Customer")
            email = body.get("email", "new.customer@keybank.com")
            username = body.get("username", f"user_{random.randint(100,999)}")
            new_id = f"CUST-{random.randint(10000,99999)}"
            new_user = {
                "id": new_id,
                "username": username,
                "name": name,
                "nameKh": f"{name} (អតិថិជនថ្មី)",
                "role": "Retail Customer",
                "roleKh": "អតិថិជនទូទៅ (Retail Customer)",
                "department": "Retail Banking",
                "email": email,
                "avatar": "".join([part[0] for part in name.split()[:2]]).upper() or "CU",
                "avatarBg": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
                "accessLevel": "CUSTOMER",
                "badgeColor": "#3b82f6"
            }
            USERS_DB[username] = new_user
            STATE["activeUser"] = new_user
            self._send_json(201, {"status": "SUCCESS", "user": new_user})
            return

        if parsed.path == "/api/chat":
            user_msg = body.get("message", "")
            session_id = body.get("sessionId", "demo-session-1")
            lang = body.get("lang", "auto")
            username = body.get("username")
            user = USERS_DB.get(username, STATE["activeUser"])
            
            result = execute_agentic_reasoning(user_msg, session_id, lang, user)
            self._send_json(200, result)
            return

        self._send_json(404, {"error": "Not Found"})

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), DemoAppHandler)
    print(f"KEY Bank Enterprise Server running on http://0.0.0.0:{PORT}")
    server.serve_forever()
