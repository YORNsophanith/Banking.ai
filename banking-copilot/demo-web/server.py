#!/usr/bin/env python3
"""
KEY Bank — Enterprise Agentic AI Banking System & Backend Server
Protected Multi-Role Authentication Server (Password Required)
AI Agent Specialist: Vichhai AI (Comprehensive Banking & Finance Knowledge Base)
Microsoft Copilot Studio Integration: Direct Line 3.0 API Client + Human Escalation Engine
Executive Board / System Administrator: Mr. Sophanith Yorn
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import re
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone
import random

PORT = int(os.environ.get("PORT", 3000))
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
KB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge-base")

# Microsoft Copilot Studio Direct Line Configuration
COPILOT_STUDIO_CONFIG = {
    "directLineSecret": os.environ.get("COPILOT_STUDIO_DIRECT_LINE_SECRET", ""),
    "tokenEndpoint": os.environ.get("COPILOT_STUDIO_TOKEN_ENDPOINT", ""),
    "environment": os.environ.get("COPILOT_STUDIO_ENVIRONMENT", "Production / Standalone Hybrid"),
    "isConnected": False,
    "lastTested": None,
    "activeConversations": {} # session_id -> { "conversationId": "...", "watermark": "..." }
}

# Pre-configured Users with Secure Passwords and Role-Specific Metadata
USERS_DB = {
    "admin": {
        "id": "USR-ADMIN-001",
        "username": "admin",
        "passwords": ["Password@123", "KeyBank@2026!"],
        "name": "Mr. Sophanith Yorn",
        "nameKh": "លោក យន សុផានីត",
        "role": "Administrator",
        "roleKh": "អគ្គនាយកគ្រប់គ្រងប្រព័ន្ធ",
        "department": "Executive Board",
        "departmentKh": "គណៈគ្រប់គ្រងជាន់ខ្ពស់",
        "email": "sophanith.yorn@keybank.com",
        "avatar": "SY",
        "avatarBg": "linear-gradient(135deg, #1e40af 0%, #1e1b4b 100%)",
        "accessLevel": "SUPER_ADMIN",
        "badgeColor": "#3b82f6",
        "dashboardTheme": "executive"
    },
    "sophanith": {
        "id": "USR-ADMIN-001",
        "username": "sophanith",
        "passwords": ["Password@123", "KeyBank@2026!"],
        "name": "Mr. Sophanith Yorn",
        "nameKh": "លោក យន សុផានីត",
        "role": "Administrator",
        "roleKh": "អគ្គនាយកគ្រប់គ្រងប្រព័ន្ធ",
        "department": "Executive Board",
        "departmentKh": "គណៈគ្រប់គ្រងជាន់ខ្ពស់",
        "email": "sophanith.yorn@keybank.com",
        "avatar": "SY",
        "avatarBg": "linear-gradient(135deg, #1e40af 0%, #1e1b4b 100%)",
        "accessLevel": "SUPER_ADMIN",
        "badgeColor": "#3b82f6",
        "dashboardTheme": "executive"
    },
    "ravith": {
        "id": "USR-FIN-002",
        "username": "ravith",
        "passwords": ["Password@123", "Finance#2026", "KeyBank@2026!"],
        "name": "Vn. Voeun Ravith",
        "nameKh": "វ.ន វឿន រ៉ាវិទ",
        "role": "Finance Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងហិរញ្ញវត្ថុ",
        "department": "Finance & Treasury",
        "departmentKh": "ផ្នែកហិរញ្ញវត្ថុ និងរតនាគារ",
        "email": "ravith.voeun@keybank.com",
        "avatar": "VR",
        "avatarBg": "linear-gradient(135deg, #059669 0%, #064e3b 100%)",
        "accessLevel": "FINANCE_ADMIN",
        "badgeColor": "#10b981",
        "dashboardTheme": "finance"
    },
    "phirek": {
        "id": "USR-MKT-003",
        "username": "phirek",
        "passwords": ["Password@123", "Market#2026", "KeyBank@2026!"],
        "name": "Vn. Hon Phirek",
        "nameKh": "វ.ន ហន ភិរ៉េក",
        "role": "Marketing Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងទីផ្សារ",
        "department": "Growth & Marketing",
        "departmentKh": "ផ្នែកពាណិជ្ជកម្ម និងទីផ្សារ",
        "email": "phirek.hon@keybank.com",
        "avatar": "HP",
        "avatarBg": "linear-gradient(135deg, #d97706 0%, #78350f 100%)",
        "accessLevel": "MARKETING_ADMIN",
        "badgeColor": "#f59e0b",
        "dashboardTheme": "marketing"
    },
    "sokny": {
        "id": "USR-IT-004",
        "username": "sokny",
        "passwords": ["Password@123", "Tech#2026", "KeyBank@2026!"],
        "name": "Mr. San Sokny",
        "nameKh": "លោក សាន សុកនី",
        "role": "IT Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងបច្ចេកវិទ្យា (IT)",
        "department": "Information Technology & Security",
        "departmentKh": "ផ្នែកបច្ចេកវិទ្យា និងសុវត្ថិភាព",
        "email": "sokny.san@keybank.com",
        "avatar": "SS",
        "avatarBg": "linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%)",
        "accessLevel": "IT_ADMIN",
        "badgeColor": "#8b5cf6",
        "dashboardTheme": "it_security"
    },
    "vathanakboth": {
        "id": "USR-SALES-005",
        "username": "vathanakboth",
        "passwords": ["Password@123", "Sales#2026", "KeyBank@2026!"],
        "name": "Mr. Ly Vathanakboth",
        "nameKh": "លោក លី វឌ្ឍនៈបថ",
        "role": "Sale Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងផ្នែកលក់",
        "department": "Retail & Corporate Sales",
        "departmentKh": "ផ្នែកលក់ និងទំនាក់ទំនងអាជីវកម្ម",
        "email": "vathanakboth.ly@keybank.com",
        "avatar": "LV",
        "avatarBg": "linear-gradient(135deg, #0284c7 0%, #0c4a6e 100%)",
        "accessLevel": "SALES_ADMIN",
        "badgeColor": "#0ea5e9",
        "dashboardTheme": "sales_manager"
    },
    "noeun_panha": {
        "id": "USR-SALES-006",
        "username": "noeun_panha",
        "passwords": ["Password@123", "SalesOff#2026", "KeyBank@2026!"],
        "name": "Mr. Noeun Panha",
        "nameKh": "លោក នឿន បញ្ញា",
        "role": "Sale Officer",
        "roleKh": "មន្ត្រីផ្នែកលក់",
        "department": "Retail Sales",
        "departmentKh": "ផ្នែកសេវាកម្មលក់",
        "email": "panha.noeun@keybank.com",
        "avatar": "NP",
        "avatarBg": "linear-gradient(135deg, #0d9488 0%, #134e4a 100%)",
        "accessLevel": "SALES_OFFICER",
        "badgeColor": "#14b8a6",
        "dashboardTheme": "sales_officer"
    },
    "panha_n": {
        "id": "USR-SALES-006",
        "username": "panha_n",
        "passwords": ["Password@123", "SalesOff#2026", "KeyBank@2026!"],
        "name": "Mr. Noeun Panha",
        "nameKh": "លោក នឿន បញ្ញា",
        "role": "Sale Officer",
        "roleKh": "មន្ត្រីផ្នែកលក់",
        "department": "Retail Sales",
        "departmentKh": "ផ្នែកសេវាកម្មលក់",
        "email": "panha.noeun@keybank.com",
        "avatar": "NP",
        "avatarBg": "linear-gradient(135deg, #0d9488 0%, #134e4a 100%)",
        "accessLevel": "SALES_OFFICER",
        "badgeColor": "#14b8a6",
        "dashboardTheme": "sales_officer"
    },
    "chea_panha": {
        "id": "USR-HR-007",
        "username": "chea_panha",
        "passwords": ["Password@123", "HrMgr#2026", "KeyBank@2026!"],
        "name": "Ms. Chea Panha",
        "nameKh": "កញ្ញា ជា បញ្ញា",
        "role": "HR Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងធនធានមនុស្ស (HR)",
        "department": "Human Resources",
        "departmentKh": "ផ្នែកគ្រប់គ្រងធនធានមនុស្ស",
        "email": "panha.chea@keybank.com",
        "avatar": "CP",
        "avatarBg": "linear-gradient(135deg, #db2777 0%, #831843 100%)",
        "accessLevel": "HR_ADMIN",
        "badgeColor": "#ec4899",
        "dashboardTheme": "hr"
    },
    "panha_c": {
        "id": "USR-HR-007",
        "username": "panha_c",
        "passwords": ["Password@123", "HrMgr#2026", "KeyBank@2026!"],
        "name": "Ms. Chea Panha",
        "nameKh": "កញ្ញា ជា បញ្ញា",
        "role": "HR Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងធនធានមនុស្ស (HR)",
        "department": "Human Resources",
        "departmentKh": "ផ្នែកគ្រប់គ្រងធនធានមនុស្ស",
        "email": "panha.chea@keybank.com",
        "avatar": "CP",
        "avatarBg": "linear-gradient(135deg, #db2777 0%, #831843 100%)",
        "accessLevel": "HR_ADMIN",
        "badgeColor": "#ec4899",
        "dashboardTheme": "hr"
    },
    "nisa": {
        "id": "USR-MKT-008",
        "username": "nisa",
        "passwords": ["Password@123", "MktOff#2026", "KeyBank@2026!"],
        "name": "Ms. Na Nisa",
        "nameKh": "កញ្ញា ណា នីសា",
        "role": "Marketing Officer",
        "roleKh": "មន្ត្រីផ្នែកទីផ្សារ",
        "department": "Growth & Marketing",
        "departmentKh": "ផ្នែកទំនាក់ទំនងទីផ្សារ",
        "email": "nisa.na@keybank.com",
        "avatar": "NN",
        "avatarBg": "linear-gradient(135deg, #ea580c 0%, #7c2d12 100%)",
        "accessLevel": "MARKETING_OFFICER",
        "badgeColor": "#f97316",
        "dashboardTheme": "marketing_officer"
    },
    "sophia": {
        "id": "CUST-10029",
        "username": "sophia",
        "passwords": ["Password@123", "Client@2026!", "KeyBank@2026!"],
        "name": "Ms. Sophia Chen",
        "nameKh": "កញ្ញា សូហ្វីយ៉ា ចិន",
        "role": "Retail Customer",
        "roleKh": "អតិថិជនកម្រិតផ្លាទីនៀម",
        "department": "Retail Banking",
        "departmentKh": "សេវាអតិថិជនទូទៅ",
        "email": "sophia.chen@example.com",
        "avatar": "SC",
        "avatarBg": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
        "accessLevel": "CUSTOMER",
        "badgeColor": "#3b82f6",
        "dashboardTheme": "customer"
    },
    "customer": {
        "id": "CUST-10029",
        "username": "customer",
        "passwords": ["Password@123", "Client@2026!", "KeyBank@2026!"],
        "name": "Alex Morgan",
        "nameKh": "Alex Morgan",
        "role": "Retail Customer",
        "roleKh": "អតិថិជនកម្រិតផ្លាទីនៀម",
        "department": "Retail Banking",
        "departmentKh": "សេវាអតិថិជនទូទៅ",
        "email": "alex.morgan@example.com",
        "avatar": "AM",
        "avatarBg": "linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)",
        "accessLevel": "CUSTOMER",
        "badgeColor": "#3b82f6",
        "dashboardTheme": "customer"
    }
}

# Live Banking State
STATE = {
    "activeUser": None,
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
            "accountType": "High-Yield Savings",
            "accountTypeKh": "គណនីសន្សំការប្រាក់ខ្ពស់",
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
            "statusKh": "សកម្ម",
            "expiry": "08/29",
            "dailyLimit": 2500,
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
            "categoryKh": "ទិញទំនិញម្ហូបអាហារ",
            "amount": -84.32,
            "status": "POSTED",
            "statusKh": "បានទូទាត់"
        },
        {
            "transactionId": "TXN-9011",
            "postedDate": "Yesterday",
            "postedDateKh": "ម្សិលមិញ",
            "merchant": "Uber Technologies Inc",
            "category": "Transport",
            "categoryKh": "សេវាធ្វើដំណើរ",
            "amount": -24.50,
            "status": "POSTED",
            "statusKh": "បានទូទាត់"
        },
        {
            "transactionId": "TXN-9010",
            "postedDate": "2 days ago",
            "postedDateKh": "២ ថ្ងៃមុន",
            "merchant": "Unknown Online Retailer - London UK",
            "category": "E-Commerce",
            "categoryKh": "ទិញទំនិញអនឡាញក្រៅប្រទេស",
            "amount": -329.99,
            "status": "FLAGGED",
            "statusKh": "សង្ស័យ"
        },
        {
            "transactionId": "TXN-9009",
            "postedDate": "Sep 26, 2026",
            "postedDateKh": "២៦ កញ្ញា ២០២៦",
            "merchant": "Direct Deposit - KEY Payroll Disburse",
            "category": "Income",
            "categoryKh": "ប្រាក់បៀវត្សរ៍ប្រចាំខែ",
            "amount": 3200.00,
            "status": "POSTED",
            "statusKh": "បានទូទាត់"
        }
    ],
    "disputes": [
        {
            "caseId": "DSP-2026-9812-01",
            "transactionId": "TXN-9010",
            "merchant": "Unknown Online Retailer - London UK",
            "amount": 329.99,
            "currency": "$",
            "reason": "Suspected Unauthorized Transaction (London, UK)",
            "reasonKh": "ប្រតិបត្តិការមិនស្គាល់ប្រភពនៅទីក្រុងឡុងដ៍",
            "status": "UNDER_INVESTIGATION",
            "statusKh": "កំពុងស៊ើបអង្កេត",
            "provisionalCredit": 329.99,
            "filedAt": "2026-09-28T14:30:00Z",
            "provisionalCreditStatus": "PROVISIONALLY_CREDITED",
            "provisionalCreditStatusKh": "បានបញ្ចូលឥណទានបណ្តោះអាសន្ន"
        }
    ],
    "escalations": [],
    "active_otp_challenges": {},
    "pending_actions": {}
}

# ==========================================
# Microsoft Copilot Studio Direct Line Client
# ==========================================
def query_copilot_studio_direct_line(user_msg, session_id, user_name):
    secret = COPILOT_STUDIO_CONFIG.get("directLineSecret", "").strip()
    if not secret:
        return None

    try:
        conv_info = COPILOT_STUDIO_CONFIG["activeConversations"].get(session_id)
        if not conv_info:
            req = urllib.request.Request(
                "https://directline.botframework.com/v3/directline/conversations",
                headers={
                    "Authorization": f"Bearer {secret}",
                    "Content-Type": "application/json"
                },
                data=b"{}",
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                conv_info = {
                    "conversationId": data["conversationId"],
                    "token": data.get("token", secret),
                    "watermark": None
                }
                COPILOT_STUDIO_CONFIG["activeConversations"][session_id] = conv_info
                COPILOT_STUDIO_CONFIG["isConnected"] = True

        conv_id = conv_info["conversationId"]
        token = conv_info.get("token", secret)

        activity_payload = {
            "type": "message",
            "from": {"id": f"user_{session_id[:8]}", "name": user_name},
            "text": user_msg
        }
        send_req = urllib.request.Request(
            f"https://directline.botframework.com/v3/directline/conversations/{conv_id}/activities",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            data=json.dumps(activity_payload).encode("utf-8"),
            method="POST"
        )
        with urllib.request.urlopen(send_req, timeout=5) as send_resp:
            pass

        watermark_param = f"?watermark={conv_info['watermark']}" if conv_info.get("watermark") else ""
        get_req = urllib.request.Request(
            f"https://directline.botframework.com/v3/directline/conversations/{conv_id}/activities{watermark_param}",
            headers={"Authorization": f"Bearer {token}"},
            method="GET"
        )
        with urllib.request.urlopen(get_req, timeout=5) as get_resp:
            act_data = json.loads(get_resp.read().decode("utf-8"))
            activities = act_data.get("activities", [])
            conv_info["watermark"] = act_data.get("watermark")

            bot_replies = []
            for act in activities:
                if act.get("from", {}).get("id") != f"user_{session_id[:8]}" and act.get("text"):
                    bot_replies.append(act["text"])

            if bot_replies:
                return {
                    "reply": "\n\n".join(bot_replies),
                    "thoughtProcess": [
                        "1. Query dispatched to Microsoft Copilot Studio (Direct Line 3.0).",
                        "2. Agent Generative Topic matched & evaluated.",
                        "3. Response stream received from Microsoft Power Platform."
                    ],
                    "card": None,
                    "source": "Microsoft Copilot Studio"
                }
    except Exception as e:
        print(f"⚠️ Copilot Studio Direct Line Notice: {e}. Falling back to internal engine.")
        COPILOT_STUDIO_CONFIG["isConnected"] = False

    return None

def is_khmer_text(text):
    return bool(re.search(r'[\u1780-\u17FF]', text))

def build_human_escalation_card(ticket_id, specialist_name, specialist_role, phone, email, is_kh=False):
    if is_kh:
        return {
            "type": "HumanEscalation",
            "ticketId": ticket_id,
            "title": "🤝 ការផ្ទេរទៅកាន់បុគ្គលិកជំនាញ / ថ្នាក់ដឹកនាំ",
            "specialist": specialist_name,
            "role": specialist_role,
            "phone": phone,
            "email": email,
            "estimatedWait": "ក្រោម ២ នាទី",
            "btnText": "📞 ហៅទូរស័ព្ទទៅកាន់ផ្នែកជំនួយផ្ទាល់"
        }
    return {
        "type": "HumanEscalation",
        "ticketId": ticket_id,
        "title": "🤝 Live Human Specialist Escalation",
        "specialist": specialist_name,
        "role": specialist_role,
        "phone": phone,
        "email": email,
        "estimatedWait": "< 2 minutes",
        "btnText": "📞 Connect to Human Agent Now"
    }

def execute_agentic_reasoning(user_text, session_id, lang_preference="auto", current_user=None):
    text = user_text.lower().strip()
    is_kh = is_khmer_text(user_text) or lang_preference == "km"
    user = current_user or USERS_DB["sophanith"]
    user_name = user.get("nameKh") if is_kh else user.get("name")
    user_role = user.get("roleKh") if is_kh else user.get("role")

    thought_process = []
    card_data = None
    reply = ""

    # Check for pending OTP verification
    if session_id in STATE["pending_actions"]:
        pending = STATE["pending_actions"][session_id]
        if "123456" in text or "123 456" in text or "otp" in text or "កូដ" in text or text.isdigit():
            action_type = pending["type"]
            thought_process.append("1. Verify Step-Up Auth OTP -> Code 123456 MATCHED.")
            thought_process.append(f"2. Execute privileged action '{action_type}'.")

            if action_type == "UNFREEZE_CARD":
                STATE["cards"][0]["status"] = "ACTIVE"
                STATE["cards"][0]["statusKh"] = "សកម្ម"
                del STATE["pending_actions"][session_id]
                
                if is_kh:
                    reply = f"✅ **ការផ្ទៀងផ្ទាត់លេខកូដបានជោគជ័យ!**\n\nកាត Visa Platinum (•••• 7711) របស់លោកអ្នកត្រូវបាន **ដោះសោ** ឱ្យដំណើរការធម្មតាវិញហើយ។ លោកអ្នកអាចធ្វើប្រតិបត្តិការទូទាត់ និងដកប្រាក់បានភ្លាមៗ។"
                else:
                    reply = f"✅ **OTP Verification Successful!**\n\nYour Visa Platinum (•••• 7711) card has been **Unfrozen** and is now fully active for transactions and withdrawals."
                
                return {
                    "reply": reply,
                    "thoughtProcess": thought_process,
                    "card": None
                }
            elif action_type == "CONFIRM_DISPUTE":
                case_id = f"DSP-2026-{random.randint(1000, 9999)}"
                STATE["cards"][0]["status"] = "FROZEN"
                STATE["cards"][0]["statusKh"] = "បានបង្កក"
                
                new_dispute = {
                    "caseId": case_id,
                    "transactionId": "TXN-9010",
                    "merchant": "Unknown Online Retailer - London UK",
                    "amount": 329.99,
                    "currency": "$",
                    "reason": "Unauthorized Foreign Transaction",
                    "reasonKh": "ប្រតិបត្តិការមិនស្គាល់ប្រភពក្រៅប្រទេស",
                    "status": "UNDER_INVESTIGATION",
                    "statusKh": "កំពុងស៊ើបអង្កេត",
                    "provisionalCredit": 329.99,
                    "filedAt": datetime.now(timezone.utc).isoformat(),
                    "provisionalCreditStatus": "PROVISIONALLY_CREDITED",
                    "provisionalCreditStatusKh": "បានបញ្ចូលឥណទានបណ្តោះអាសន្ន"
                }
                STATE["disputes"].append(new_dispute)
                del STATE["pending_actions"][session_id]

                if is_kh:
                    reply = (
                        f"🛡️ **ពាក្យបណ្តឹងតវ៉ារបស់លោកអ្នកត្រូវបានបង្កើតដោយជោគជ័យ!**\n\n"
                        f"• **លេខសំណុំរឿង:** `{case_id}`\n"
                        f"• **ចំនួនទឹកប្រាក់តវ៉ា:** $329.99 (Unknown Online Retailer - London UK)\n"
                        f"• **ឥណទានបណ្តោះអាសន្ន:** $329.99 ត្រូវបានបញ្ចូលជូនគណនីចរន្ត (*9812)\n"
                        f"• **ស្ថានភាពកាត:** កាត Visa ត្រូវបាន **បង្កក** ជាស្វ័យប្រវត្តដើម្បីការពារហានិភ័យបន្ត។"
                    )
                else:
                    reply = (
                        f"🛡️ **Fraud Dispute Filed Successfully!**\n\n"
                        f"• **Case Number:** `{case_id}`\n"
                        f"• **Disputed Amount:** $329.99 (Unknown Online Retailer - London UK)\n"
                        f"• **Provisional Credit:** $329.99 credited to Checking (*9812)\n"
                        f"• **Card Status:** Visa card has been **FROZEN** to prevent further fraudulent attempts."
                    )
                
                return {
                    "reply": reply,
                    "thoughtProcess": thought_process,
                    "card": None
                }

    # Optional Copilot Studio Direct Line Query
    copilot_res = query_copilot_studio_direct_line(user_text, session_id, user_name)
    if copilot_res:
        return copilot_res

    # Intent 0: Direct Request to Speak to Human / Escalation
    if any(k in text for k in [
        "speak to human", "talk to agent", "human specialist", "real person", "representative", 
        "escalate", "support agent", "customer service officer", "transfer to human",
        "ជួបបុគ្គលិក", "និយាយជាមួយមនុស្ស", "ផ្ទេរទៅបុគ្គលិក", "ជំនួយការផ្ទាល់", "ទាក់ទងមនុស្ស", "តំណាងសេវា"
    ]):
        ticket_id = f"ESC-2026-{random.randint(1000, 9999)}"
        thought_process.append("1. Trigger Copilot Studio Escalate Topic / Human Agent Handoff.")
        thought_process.append(f"2. Generate VIP Support Ticket -> {ticket_id}.")
        thought_process.append("3. Match assigned departmental specialist.")

        STATE["escalations"].append({
            "ticketId": ticket_id,
            "customer": user.get("name"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "QUEUED"
        })

        card_data = build_human_escalation_card(
            ticket_id=ticket_id,
            specialist_name="Mr. San Sokny (IT & Security) / Mr. Ly Vathanakboth (Sales)",
            specialist_role="Senior Escalation Officer",
            phone="+855 12 888 999",
            email="support.escalation@keybank.com",
            is_kh=is_kh
        )

        if is_kh:
            reply = (
                f"🤝 **សំណើផ្ទេរទៅកាន់បុគ្គលិកជំនាញផ្ទាល់:**\n\n"
                f"ខ្ញុំបានបង្កើតសំបុត្រជំនួយលេខ `{ticket_id}` ជូនលោកអ្នករួចរាល់ហើយ។ បុគ្គលិកជំនាញធនាគារ KEY Bank នឹងចូលរួមជជែក ឬទាក់ទងមកលោកអ្នកក្នុងរយៈពេល **ក្រោម ២ នាទី**។\n\n"
                f"• **លេខកូដសំបុត្រ:** `{ticket_id}`\n"
                f"• **ផ្នែកទទួលបន្ទុក:** ផ្នែកដោះស្រាយវិវាទ និងសេវាអតិថិជនជាន់ខ្ពស់\n"
                f"• **លេខទូរស័ព្ទទាន់ហេតុការណ៍:** `+855 12 888 999` (២៤/៧)"
            )
        else:
            reply = (
                f"🤝 **Connecting You to a Live Banking Specialist:**\n\n"
                f"I have initialized an escalation ticket `{ticket_id}` for you. A dedicated KEY Bank senior representative is joining your session within **< 2 minutes**.\n\n"
                f"• **Escalation Ticket ID:** `{ticket_id}`\n"
                f"• **Assigned Queue:** Priority Customer Resolution & Disputes Desk\n"
                f"• **Direct 24/7 Hotline:** `+855 12 888 999`"
            )

    # Intent 1: Fixed Deposit / Term Deposit Rates & Savings APY
    elif any(k in text for k in ["fixed deposit", "term deposit", "interest rate", "interest", "apy", "rate", "rates", "yield", "សន្សំមានកាលកំណត់", "បញ្ញើមានកាលកំណត់", "អត្រាការប្រាក់", "ការប្រាក់"]):
        thought_process.append("1. Query Knowledge Base: retail_and_commercial_products.md.")
        thought_process.append("2. Retrieve Term Deposit Schedule (USD & KHR rates up to 8.00%).")

        if is_kh:
            reply = (
                f"📈 **តារាងអត្រាការប្រាក់បញ្ញើមានកាលកំណត់ (Fixed Term Deposit):**\n\n"
                f"• **កាលកំណត់ ៣ ខែ:** ៤.៥០% ក្នុងមួយឆ្នាំ (USD) | ៥.៥០% ក្នុងមួយឆ្នាំ (KHR)\n"
                f"• **កាលកំណត់ ៦ ខែ:** ៥.២៥% ក្នុងមួយឆ្នាំ (USD) | ៦.២៥% ក្នុងមួយឆ្នាំ (KHR)\n"
                f"• **កាលកំណត់ ១២ ខែ (១ ឆ្នាំ):** **៦.៥០% ក្នុងមួយឆ្នាំ (USD)** | **៧.២៥% ក្នុងមួយឆ្នាំ (KHR)**\n"
                f"• **កាលកំណត់ ២៤ ខែ (២ ឆ្នាំ):** **៦.៨៥% ក្នុងមួយឆ្នាំ (USD)** | **៧.៧៥% ក្នុងមួយឆ្នាំ (KHR)**\n"
                f"• **កាលកំណត់ ៣៦ ខែ (៣ ឆ្នាំ):** **៧.១៥% ក្នុងមួយឆ្នាំ (USD)** | **៨.០០% ក្នុងមួយឆ្នាំ (KHR)**\n\n"
                f"💡 *ការទូទាត់ការប្រាក់អាចជ្រើសរើសទទួលជារៀងរាល់ខែ ឬទទួលសរុបនៅពេលផុតកំណត់។ គណនីសន្សំទូទៅទទួលបានការប្រាក់ ៤.៧៥% ក្នុងមួយឆ្នាំ (USD) / ៥.២៥% (KHR)។ ប្រាក់រៀលទទួលបានផលចំណេញខ្ពស់បំផុត!*"
            )
        else:
            reply = (
                f"📈 **KEY Bank Fixed Term Deposit Rate Schedule:**\n\n"
                f"• **3-Month Term:** 4.50% p.a. (USD) | 5.50% p.a. (KHR)\n"
                f"• **6-Month Term:** 5.25% p.a. (USD) | 6.25% p.a. (KHR)\n"
                f"• **12-Month Term (1 Year):** **6.50% p.a. (USD)** | **7.25% p.a. (KHR)**\n"
                f"• **24-Month Term (2 Years):** **6.85% p.a. (USD)** | **7.75% p.a. (KHR)**\n"
                f"• **36-Month Term (3 Years):** **7.15% p.a. (USD)** | **8.00% p.a. (KHR)**\n\n"
                f"💡 *Interest can be paid monthly into your Checking account or compounded at maturity. Standard High-Yield Savings earns 4.75% APY (USD) / 5.25% APY (KHR). Maximize yield with KHR deposits!*"
            )

    # Intent 2: Payment Cards, Credit Limit, Grace Period & Fees
    elif any(k in text for k in ["card limit", "grace period", "credit card", "pos limit", "atm limit", "រយៈពេលអនុគ្រោះ", "កាតឥណទាន", "ដែនកំណត់កាត", "ប័ណ្ណឥណទាន"]):
        thought_process.append("1. Query Knowledge Base: cards_emv_and_digital_wallets.md.")
        thought_process.append("2. Extract Card Specifications, 45-day grace period, and POS/ATM limits.")

        if is_kh:
            reply = (
                f"💳 **ព័ត៌មានលម្អិតអំពីកាត Visa Platinum របស់ KEY Bank:**\n\n"
                f"• **រយៈពេលអនុគ្រោះឥតគិតការប្រាក់:** រហូតដល់ **៤៥ ថ្ងៃ (45-Day Grace Period)** សម្រាប់ការទូទាត់ពេញចំនួន\n"
                f"• **អត្រាការប្រាក់បង្វិល (Revolving Interest):** ១៨% ក្នុងមួយឆ្នាំ (១.៥០% ក្នុងមួយខែ)\n"
                f"• **ការទូទាត់អប្បបរមាប្រចាំខែ:** ៥% នៃសមតុល្យជំពាក់ ឬ ១០.០០ ដុល្លារ\n"
                f"• **ដែនកំណត់ដកប្រាក់ ATM ប្រចាំថ្ងៃ:** **១,០០០.០០ ដុល្លារ / ថ្ងៃ**\n"
                f"• **ដែនកំណត់ទូទាត់តាមម៉ាស៊ីន POS/Online:** **៥,០០០.០០ ដុល្លារ / ថ្ងៃ**\n"
                f"• **បច្ចេកវិទ្យាសុវត្ថិភាព:** EMV Chip, Contactless NFC, និង 3D Secure 2.0"
            )
        else:
            reply = (
                f"💳 **KEY Bank Visa Platinum Card Specifications:**\n\n"
                f"• **Interest-Free Grace Period:** Up to **45 Days** on full statement balance settlements\n"
                f"• **Revolving APR:** 18.00% p.a. (1.50% monthly) on carried balances\n"
                f"• **Minimum Monthly Payment:** 5% of statement balance or $10.00 USD (whichever is greater)\n"
                f"• **Daily ATM Withdrawal Limit:** **$1,000.00 USD / day**\n"
                f"• **Daily POS / Online Limit:** **$5,000.00 USD / day**\n"
                f"• **Security Protocols:** EMV Chip & PIN, Visa Contactless, and 3D Secure OTP authentication"
            )

    # Intent 3: Mortgages, Home Loans & SME Credit
    elif any(k in text for k in ["loan", "mortgage", "housing", "borrow", "credit score", "cbc", "dsr", "sme", "កម្ចី", "ឥណទានគេហដ្ឋាន", "ឥណទានកម្ចី", "ទិញផ្ទះ", "ខ្ចីប្រាក់", "ខ្ចីលុយ", "កម្ចីផ្ទាល់ខ្លួន", "កម្ចីអាជីវកម្ម"]):
        thought_process.append("1. Query Knowledge Base: lending_mortgages_and_credit.md.")
        thought_process.append("2. Synthesize Mortgage, Personal Loan, and DSR underwriting guidelines.")

        if is_kh:
            reply = (
                f"🏠 **សេវាឥណទាន និងកម្ចីធនាគារ KEY Bank:**\n\n"
                f"១. **កម្ចីទិញគេហដ្ឋាន (Home Mortgage):**\n"
                f"   • អត្រាការប្រាក់ចាប់ពី **៦.៩៩% ក្នុងមួយឆ្នាំ** (កម្ចីផ្ទះបៃតង ៦.៥០%)\n"
                f"   • ទំហំកម្ចីរហូតដល់ **៨០% នៃតម្លៃអចលនទ្រព្យ (LTV 80%)**\n"
                f"   • រយៈពេលសងរហូតដល់ **២៥ ឆ្នាំ (៣០០ ខែ)**\n\n"
                f"២. **កម្ចីផ្ទាល់ខ្លួនគ្មានទ្រព្យធានា (Personal Loan):**\n"
                f"   • ទំហំកម្ចីពី ១,០០០ ដល់ **២៥,០០០ ដុល្លារ** (ផ្អែកលើប្រាក់បៀវត្សរ៍)\n"
                f"   • ប្រាក់ចំណូលប្រចាំខែអប្បបរមា ៤០០ ដុល្លារ\n\n"
                f"៣. **កម្ចីអាជីវកម្មខ្នាតតូច និងមធ្យម (SME Business Loan):**\n"
                f"   • ទំហំកម្ចីពី ១០,០០០ ដល់ **១,០០០,០០០ ដុល្លារ+** (ការប្រាក់ចាប់ពី ៧.៥០% ឡើងទៅ)\n\n"
                f"📋 *លក្ខខណ្ឌតម្រូវ៖ អត្តសញ្ញាណប័ណ្ណ, សៀវភៅស្នាក់នៅ/គ្រួសារ, លិខិតបញ្ជាក់ប្រាក់ចំណូល ៦ ខែ, និងរបាយការណ៍ CBC ល្អ (DSR អតិបរមា ៥០%)។*"
            )
        else:
            reply = (
                f"🏠 **KEY Bank Lending & Financing Solutions:**\n\n"
                f"1. **Home Mortgage Loans:**\n"
                f"   • Interest rates starting at **6.99% p.a.** (Eco-Green mortgages from 6.50%)\n"
                f"   • Loan-to-Value (LTV) up to **80%** of appraised property value\n"
                f"   • Repayment tenure up to **25 Years (300 Months)**\n\n"
                f"2. **Personal Unsecured Consumer Loans:**\n"
                f"   • Borrow from $1,000 up to **$25,000 USD** (No collateral required)\n"
                f"   • Minimum verified salary: $400/month\n\n"
                f"3. **SME & Commercial Credit Facilities:**\n"
                f"   • Working capital and term loans from $10,000 up to **$1,000,000 USD+** (from 7.50% p.a.)\n\n"
                f"📋 *Eligibility: Valid ID/Passport, 6 months salary/business bank statements, and maximum Debt-Service Ratio (DSR) of 50%.*"
            )

    # Intent 4: Bakong KHQR, Wire Transfers & Remittance Fees
    elif any(k in text for k in ["bakong", "khqr", "transfer fee", "wire", "swift", "remittance", "fee", "fees", "ថ្លៃផ្ទេរប្រាក់", "បាគង", "ថ្លៃសេវា", "សេវាផ្ទេរ"]):
        thought_process.append("1. Query Knowledge Base: retail_and_commercial_products.md.")
        thought_process.append("2. Extract Bakong KHQR, ACH, and SWIFT wire fee policies.")

        if is_kh:
            reply = (
                f"💸 **គោលការណ៍ផ្ទេរប្រាក់ និងថ្លៃសេវាធនាគារ KEY Bank:**\n\n"
                f"• **ការផ្ទេរប្រាក់ផ្ទៃក្នុង KEY Bank:** **ឥតគិតថ្លៃ (០.០០ ដុល្លារ)** ភ្លាមៗ ២៤/៧\n"
                f"• **ការផ្ទេរប្រាក់តាម Bakong KHQR:** **ឥតគិតថ្លៃ (០.០០ ដុល្លារ)** ទៅកាន់គ្រប់ធនាគារក្នុងស្រុក\n"
                f"• **ការទូទាត់ឆ្លងដែន Bakong:** អាចស្កេនទូទាត់នៅប្រទេសថៃ (PromptPay), វៀតណាម (NAPAS), ឡាវ (LAPNet), និងម៉ាឡេស៊ី (DuitNow)\n"
                f"• **ការផ្ទេរប្រាក់ទៅក្រៅប្រទេស (Outbound SWIFT Wire):** **២៥.០០ ដុល្លារ** ក្នុងមួយប្រតិបត្តិការ\n"
                f"• **ការទទួលប្រាក់ពីក្រៅប្រទេស (Inbound SWIFT Wire):** **៥.០០ ដុល្លារ** ក្នុងមួយប្រតិបត្តិការ\n"
                f"• **ដែនកំណត់ផ្ទេរប្រាក់ប្រចាំថ្ងៃ:** រហូតដល់ ១០,០០០ ដុល្លារ / ថ្ងៃ (ឬ ៥០,០០០ ដុល្លារសម្រាប់គណនីអាជីវកម្ម)"
            )
        else:
            reply = (
                f"💸 **KEY Bank Transfers & Remittance Schedule:**\n\n"
                f"• **Internal KEY Bank Transfers:** **$0.00 (Free)** instant 24/7\n"
                f"• **Bakong KHQR Interbank Transfers:** **$0.00 (Free)** to all participating local banks\n"
                f"• **Bakong Cross-Border QR:** Zero-fee scanning in Thailand (PromptPay), Vietnam (NAPAS), Laos (LAPNet), and Malaysia (DuitNow)\n"
                f"• **Outbound SWIFT International Wire:** **$25.00 flat fee** per transaction\n"
                f"• **Inbound SWIFT Remittance:** **$5.00** processing fee\n"
                f"• **Daily Retail Transfer Limit:** $10,000 USD / 40,000,000 KHR per day"
            )

    # Intent 5: Inquire London $329 Transaction / Dispute / Fraud
    elif any(k in text for k in ["329", "london", "unauthorized", "suspicious", "charge", "unknown", "ឡុងដ៍", "កាត់ប្រាក់", "បន្លំ", "dispute", "fraud", "តវ៉ា", "មិនស្គាល់", "កាត់លុយខុស"]):
        thought_process.append("1. Detect transaction lookup request for $329.99 London charge.")
        thought_process.append("2. Execute Tool: GET /transactions?status=FLAGGED.")
        thought_process.append("3. Cross-reference Dispute Policy: Unrecognized foreign transaction -> Flag for fraud review.")

        if is_kh:
            reply = (
                f"⚠️ **ការរកឃើញប្រតិបត្តិការសង្ស័យ:**\n\n"
                f"យើងខ្ញុំបានរកឃើញប្រតិបត្តិការកាត់ប្រាក់ចំនួន **$329.99** កាលពី ២ ថ្ងៃមុន នៅហាង **Unknown Online Retailer** (London, United Kingdom)។\n\n"
                f"ប្រសិនបើលោកអ្នកមិនបានធ្វើប្រតិបត្តិការនេះទេ សូមចុចប៊ូតុង **ដាក់ពាក្យតវ៉ា និងបង្កកកាត** ខាងក្រោមភ្លាមៗ។ ធនាគារ KEY Bank នឹងផ្តល់ **ឥណទានបណ្តោះអាសន្ន** ជូនលោកអ្នកភ្លាមៗ។"
            )
            card_data = {
                "type": "TransactionHighlight",
                "merchant": "Unknown Online Retailer - London UK",
                "amount": "-$329.99 USD",
                "date": "២ ថ្ងៃមុន",
                "btnText": "🚨 ដាក់ពាក្យតវ៉ា និងបង្កកកាត"
            }
        else:
            reply = (
                f"⚠️ **Flagged Suspicious Transaction Detected:**\n\n"
                f"We identified a transaction for **$329.99** posted 2 days ago by **Unknown Online Retailer** in London, United Kingdom.\n\n"
                f"If you did not authorize this charge, you can file an immediate dispute below. Under Regulation E and KEY Bank policy, a **Provisional Credit of $329.99** will be issued to your account."
            )
            card_data = {
                "type": "TransactionHighlight",
                "merchant": "Unknown Online Retailer - London UK",
                "amount": "-$329.99 USD",
                "date": "2 days ago • Cross-Border",
                "btnText": "🚨 File Dispute & Freeze Card"
            }

    # Intent 6: Unfreeze Card (Requires Step-Up OTP)
    elif any(k in text for k in ["unfreeze", "unlock card", "unlock", "ដោះសោរ", "ដោះសោកាត", "បើកកាត"]):
        thought_process.append("1. Extract unfreeze intent -> High-Risk Privileged Action.")
        thought_process.append("2. Trigger Step-Up MFA Challenge -> POST /auth/step-up-challenge.")
        
        STATE["pending_actions"][session_id] = {
            "type": "UNFREEZE_CARD",
            "initiated_at": datetime.now(timezone.utc).isoformat()
        }

        if is_kh:
            reply = (
                f"🔐 **តម្រូវឱ្យមានការផ្ទៀងផ្ទាត់សុវត្ថិភាព (MFA OTP)៖**\n\n"
                f"ដើម្បីដោះសោកាត Visa Platinum (•••• 7711) សូមបញ្ចូលលេខកូដ ៦ ខ្ទង់ដែលបានផ្ញើទៅកាន់ទូរស័ព្ទរបស់លោកអ្នក (+855 •• ••• 888)។\n\n"
                f"*(សម្រាប់គំរូសាកល្បងនេះ លេខកូដគឺ៖ `123456`)*"
            )
            card_data = {
                "type": "OtpChallenge",
                "title": "បញ្ចូលលេខកូដសុវត្ថិភាព ៦ ខ្ទង់",
                "phone": "+855 •• ••• 888",
                "btnText": "បញ្ចូលលេខកូដ: 123456"
            }
        else:
            reply = (
                f"🔐 **Step-Up Authentication Required (MFA OTP):**\n\n"
                f"To unfreeze Visa Platinum (•••• 7711), please enter the 6-digit one-time passcode sent to your registered mobile device (+855 •• ••• 888).\n\n"
                f"*(For this Demo session, the verification code is: `123456`)*"
            )
            card_data = {
                "type": "OtpChallenge",
                "title": "Enter 6-Digit OTP Code",
                "phone": "+855 •• ••• 888",
                "btnText": "Submit OTP: 123456"
            }

    # Intent 7: Freeze Card
    elif any(k in text for k in ["freeze", "lock card", "block card", "បង្កក", "ចាក់សោរកាត", "បិទកាត"]):
        thought_process.append("1. Extract card lock command -> CARD-VISA-7711.")
        thought_process.append("2. Execute Core Action: POST /cards/CARD-VISA-7711/freeze.")
        
        STATE["cards"][0]["status"] = "FROZEN"
        STATE["cards"][0]["statusKh"] = "បានបង្កក"

        if is_kh:
            reply = (
                f"🔒 **កាត Visa Platinum (•••• 7711) ត្រូវបានបង្កកដោយជោគជ័យ!**\n\n"
                f"រាល់ការទូទាត់ និងដកប្រាក់តាមកាតត្រូវបានផ្អាកជាបណ្តោះអាសន្ន។ លោកអ្នកអាចដោះសោកាតវិញបានគ្រប់ពេលវេលា ដោយគ្រាន់តែបញ្ជាក់លេខកូដសុវត្ថិភាព OTP។"
            )
        else:
            reply = (
                f"🔒 **Visa Platinum (•••• 7711) has been successfully FROZEN!**\n\n"
                f"All recurring debits, POS transactions, and ATM withdrawals are now blocked. You can unfreeze your card at any time via 2FA verification."
            )

    # Intent 8: Travel Notice
    elif any(k in text for k in ["travel", "japan", "flight", "trip", "destination", "ធ្វើដំណើរ", "ជប៉ុន", "ក្រៅប្រទេស"]):
        thought_process.append("1. Extract travel intent -> Set overseas destination exemption.")
        thought_process.append("2. Invoke Core Action: POST /cards/CARD-VISA-7711/travel-notice.")
        
        destination_name = "Japan (Oct 2026)"
        if "japan" in text or "ជប៉ុន" in text:
            destination_name = "Japan (Oct 2026)"
        elif "usa" in text or "us" in text or "អាមេរិក" in text:
            destination_name = "United States (Oct 2026)"
        elif "singapore" in text or "សិង្ហបុរី" in text:
            destination_name = "Singapore (Oct 2026)"
        else:
            destination_name = "International (Oct 2026)"

        STATE["cards"][0]["travelNotice"] = destination_name

        if is_kh:
            reply = (
                f"✈️ **ការកំណត់ការធ្វើដំណើរត្រូវបានរក្សាទុកដោយជោគជ័យ!**\n\n"
                f"យើងខ្ញុំបានកត់ត្រាការជូនដំណឹងធ្វើដំណើរទៅកាន់ **{destination_name}** សម្រាប់កាត Visa Platinum (•••• 7711) របស់លោកអ្នក។ ប្រតិបត្តិការទូទាត់នៅក្រៅប្រទេសនឹងមិនត្រូវបានរារាំងដោយប្រព័ន្ធសុវត្ថិភាពស្វ័យប្រវត្តិនោះទេ។"
            )
        else:
            reply = (
                f"✈️ **Travel Notice Successfully Activated!**\n\n"
                f"A travel exemption for **{destination_name}** has been applied to your Visa Platinum (•••• 7711). Foreign card authorizations will proceed smoothly without automated fraud blocks."
            )

    # Intent 9: Recent Transactions & Activity
    elif any(k in text for k in ["recent transactions", "transaction", "transactions", "activity", "statement", "history", "ប្រតិបត្តិការ", "ប្រវត្តិ", "ចុងក្រោយ", "ចំណាយ", "ទិញអីខ្លះ"]):
        thought_process.append("1. Query Core Banking Action: GET /accounts/ACC-CHK-9812/transactions.")
        thought_process.append("2. Format recent transaction statement list.")

        txns = STATE["transactions"][:4]
        if is_kh:
            lines = [f"• **{t.get('merchant', 'Merchant')}**: `${abs(t['amount']):,.2f}` ({t.get('postedDateKh', t.get('postedDate'))}) — [{t.get('statusKh', t.get('status'))}]" for t in txns]
            reply = (
                f"📋 **ប្រតិបត្តិការថ្មីៗចុងក្រោយរបស់លោកអ្នក (*9812):**\n\n" +
                "\n".join(lines) +
                "\n\n💡 *ប្រសិនបើមានប្រតិបត្តិការណាមួយគួរឱ្យសង្ស័យ លោកអ្នកអាចប្រាប់ខ្ញុំដើម្បីដាក់ពាក្យតវ៉ាភ្លាមៗ។*"
            )
        else:
            lines = [f"• **{t.get('merchant', 'Merchant')}**: `${abs(t['amount']):,.2f}` ({t.get('postedDate')}) — [{t.get('status')}]" for t in txns]
            reply = (
                f"📋 **Recent Account Transactions (*9812):**\n\n" +
                "\n".join(lines) +
                "\n\n💡 *If you see an unfamiliar charge, simply let me know to file an immediate dispute.*"
            )

    # Intent 10: Department / Manager Routing & Staff Escalations
    elif any(k in text for k in ["manager", "director", "leadership", "contact", "executive", "it manager", "finance manager", "hr manager", "sale manager", "នាយក", "ប្រធាន", "បុគ្គលិក", "ទំនាក់ទំនង", "ថ្នាក់ដឹកនាំ", "សុផានីត", "sophanith"]):
        thought_process.append("1. Query Knowledge Base: customer_service_sop_and_escalations.md.")
        thought_process.append("2. Match departmental management directory.")

        if is_kh:
            reply = (
                f"👥 **បញ្ជីទំនាក់ទំនងថ្នាក់ដឹកនាំ និងនាយកដ្ឋាន KEY Bank:**\n\n"
                f"• **អគ្គនាយកគ្រប់គ្រងប្រព័ន្ធ:** **លោក យន សុផានីត** (`sophanith.yorn@keybank.com`)\n"
                f"• **ប្រធានគ្រប់គ្រងហិរញ្ញវត្ថុ:** **វ.ន វឿន រ៉ាវិទ** (`ravith.voeun@keybank.com`)\n"
                f"• **ប្រធានគ្រប់គ្រងទីផ្សារ:** **វ.ន ហន ភិរ៉េក** (`phirek.hon@keybank.com`)\n"
                f"• **ប្រធានគ្រប់គ្រងបច្ចេកវិទ្យា (IT):** **លោក សាន សុកនី** (`sokny.san@keybank.com`)\n"
                f"• **ប្រធានគ្រប់គ្រងផ្នែកលក់:** **លោក លី វឌ្ឍនៈបថ** (`vathanakboth.ly@keybank.com`)\n"
                f"• **ប្រធានគ្រប់គ្រងធនធានមនុស្ស (HR):** **កញ្ញា ជា បញ្ញា** (`panha.chea@keybank.com`)\n"
                f"• **មន្ត្រីផ្នែកលក់ & ទីផ្សារ:** **លោក នឿន បញ្ញា** & **កញ្ញា ណា នីសា**"
            )
        else:
            reply = (
                f"👥 **KEY Bank Leadership & Escalation Directory:**\n\n"
                f"• **Executive Administrator:** **Mr. Sophanith Yorn** (`sophanith.yorn@keybank.com`)\n"
                f"• **Finance Manager:** **Vn. Voeun Ravith** (`ravith.voeun@keybank.com`)\n"
                f"• **Marketing Manager:** **Vn. Hon Phirek** (`phirek.hon@keybank.com`)\n"
                f"• **IT & Cyber Security Manager:** **Mr. San Sokny** (`sokny.san@keybank.com`)\n"
                f"• **Sales Manager:** **Mr. Ly Vathanakboth** (`vathanakboth.ly@keybank.com`)\n"
                f"• **HR Manager:** **Ms. Chea Panha** (`panha.chea@keybank.com`)\n"
                f"• **Officers:** **Mr. Noeun Panha** (Sales) & **Ms. Na Nisa** (Marketing)"
            )

    # Intent 11: Check Balances & Accounts
    elif any(k in text for k in ["balance", "balances", "how much money", "check account", "my account", "my money", "checking", "savings", "សមតុល្យ", "សមតុល្យគណនី", "ពិនិត្យគណនី", "មើលលុយ", "ពិនិត្យលុយ", "លុយសល់ប៉ុន្មាន", "គណនីរបស់ខ្ញុំ"]):
        thought_process.append("1. Query Core Banking Action: GET /accounts/ACC-CHK-9812/balance.")
        thought_process.append("2. Format multi-account summary.")

        chk = STATE["accounts"][0]
        sav = STATE["accounts"][1]

        if is_kh:
            reply = (
                f"សូមគោរពជម្រាបជូន **{user_name}** ({user_role})! ខាងក្រោមនេះជាសមតុល្យគណនីបច្ចុប្បន្នរបស់លោកអ្នក៖\n\n"
                f"• **{chk['accountTypeKh']} (*9812):** `${chk['availableBalance']:,.2f}` (អាចប្រើប្រាស់បានភ្លាមៗ)\n"
                f"• **{sav['accountTypeKh']} (*4109):** `${sav['availableBalance']:,.2f}` (អត្រាការប្រាក់ ៤.៧៥% ក្នុងមួយឆ្នាំ)\n\n"
                f"💰 **ទ្រព្យសកម្មសរុប:** `${chk['availableBalance'] + sav['availableBalance']:,.2f}`"
            )
        else:
            reply = (
                f"Here is your current balance summary, **{user_name}** ({user_role}):\n\n"
                f"• **{chk['accountType']} (*9812):** `${chk['availableBalance']:,.2f}` Available\n"
                f"• **{sav['accountType']} (*4109):** `${sav['availableBalance']:,.2f}` (+4.75% APY)\n\n"
                f"💰 **Total Liquid Assets:** `${chk['availableBalance'] + sav['availableBalance']:,.2f}`"
            )

    # Default Fallback with Quick Escalate Action
    else:
        thought_process.append(f"1. Generative Banking Domain Analysis for {user_name}.")
        thought_process.append("2. Synthesize comprehensive banking knowledge from Vichhai AI Knowledge Base.")

        if is_kh:
            reply = (
                f"សូមគោរពជម្រាបជូន **{user_name}** ({user_role})! ខ្ញុំជា **Vichhai AI** ជំនួយការឆ្លាតវៃនៃធនាគារ KEY Bank។\n\n"
                f"ខ្ញុំបានបណ្តុះបណ្តាលចំណេះដឹងពេញលេញលើសេវាធនាគារ និងហិរញ្ញវត្ថុ។ លោកអ្នកអាចសួរខ្ញុំអំពី៖\n"
                f"• **គណនី និងការប្រាក់:** ពិនិត្យសមតុល្យ, អត្រាការប្រាក់សន្សំ ៤.៧៥% ឬបញ្ញើមានកាលកំណត់ ៧.២៥% (USD) / ៨.០០% (KHR)\n"
                f"• **សេវាឥណទាន និងកម្ចី:** កម្ចីទិញផ្ទះ (៦.៩៩%), កម្ចីផ្ទះបៃតង (៦.៥០%), កម្ចីផ្ទាល់ខ្លួន (រហូតដល់ $25k), ឬកម្ចីអាជីវកម្ម SME\n"
                f"• **ការផ្ទេរប្រាក់ និងទូទាត់:** ផ្ទេរប្រាក់តាម Bakong KHQR ឥតគិតថ្លៃ, ស្កេនទូទាត់នៅប្រទេសថៃ/វៀតណាម/ឡាវ/ម៉ាឡេស៊ី, ថ្លៃផ្ទេរប្រាក់ SWIFT $25\n"
                f"• **ការគ្រប់គ្រងកាត និងសុវត្ថិភាព:** បង្កក ឬដោះសោកាត Visa, រយៈពេលអនុគ្រោះ ៤៥ ថ្ងៃ, ដោះស្រាយប្រតិបត្តិការសង្ស័យ\n"
                f"• **ជំនួយការផ្ទាល់ (Human Escalation):** ប្រសិនបើត្រូវការជួបបុគ្គលិកជំនាញ សូមវាយពាក្យ *'ជួបបុគ្គលិក'* ដើម្បីផ្ទេរភ្លាមៗ!"
            )
        else:
            reply = (
                f"Hello **{user_name}** ({user_role})! I am **Vichhai AI**, your intelligent banking & finance specialist at KEY Bank.\n\n"
                f"I am fully equipped with real-world banking knowledge. You can ask me about:\n"
                f"• **Accounts & Deposits:** Live balance checks, High-Yield Savings (4.75% APY), or Fixed Term Deposits (up to 7.25% USD / 8.00% KHR)\n"
                f"• **Lending & Mortgages:** Home loans (from 6.99% p.a.), Eco-Green Mortgages (6.50%), Personal loans (up to $25k), or SME credit lines\n"
                f"• **Transfers & Payments:** Instant $0.00 Bakong KHQR transfers, Cross-border QR in Thailand/Vietnam/Laos/Malaysia, SWIFT wire rules\n"
                f"• **Card Controls & Fraud:** Instant Visa freeze/unfreeze, 45-day grace period, travel notices, and unauthorized dispute resolution\n"
                f"• **Human Escalation:** Need a human representative? Simply ask *'speak to human'* to be transferred to a live specialist!"
            )

    return {
        "reply": reply,
        "thoughtProcess": thought_process,
        "card": card_data,
        "source": "Vichhai AI Banking Engine"
    }

class DemoAppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def _send_json(self, status_code, data):
        response = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/api/state":
            self._send_json(200, STATE)
            return

        if parsed.path == "/api/users":
            safe_users = []
            seen_ids = set()
            for u in USERS_DB.values():
                if u["id"] not in seen_ids:
                    seen_ids.add(u["id"])
                    safe_users.append({k: v for k, v in u.items() if k != "passwords"})
            self._send_json(200, {"status": "SUCCESS", "users": safe_users})
            return

        # Copilot Studio Connection Status Endpoint
        if parsed.path == "/api/copilot/status":
            has_secret = bool(COPILOT_STUDIO_CONFIG.get("directLineSecret"))
            has_endpoint = bool(COPILOT_STUDIO_CONFIG.get("tokenEndpoint"))
            self._send_json(200, {
                "status": "CONNECTED" if (has_secret or has_endpoint) else "STANDALONE_READY",
                "copilotStudioIntegration": {
                    "directLineConfigured": has_secret,
                    "tokenEndpointConfigured": has_endpoint,
                    "environment": COPILOT_STUDIO_CONFIG.get("environment"),
                    "agent": "Vichhai AI (វិច្ឆ័យ AI)",
                    "hybridFallbackActive": True,
                    "connectedChannel": "Direct Line 3.0 REST API",
                    "openApiSpec": "/openapi/banking-core-api.json"
                }
            })
            return

        if parsed.path == "/api/health" or parsed.path == "/healthz":
            self._send_json(200, {
                "status": "UP",
                "service": "KEY Bank Enterprise AI Demo",
                "agent": "Vichhai AI",
                "admin": "Mr. Sophanith Yorn",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            return

        if parsed.path == "/api/reset":
            STATE["cards"][0]["status"] = "ACTIVE"
            STATE["cards"][0]["statusKh"] = "សកម្ម"
            STATE["cards"][0]["travelNotice"] = None
            STATE["accounts"][0]["availableBalance"] = 4520.50
            STATE["accounts"][1]["availableBalance"] = 28450.00
            self._send_json(200, {"message": "State reset successfully", "state": STATE})
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length).decode('utf-8')) if length > 0 else {}

        # 1. STRICT USERNAME & PASSWORD LOGIN
        if parsed.path == "/api/login":
            username = body.get("username", "").strip().lower()
            password = body.get("password", "").strip()

            user = USERS_DB.get(username)
            if user and (password in user.get("passwords", []) or password == user.get("password")):
                STATE["activeUser"] = user
                safe_user = {k: v for k, v in user.items() if k != "passwords"}
                self._send_json(200, {
                    "status": "SUCCESS",
                    "success": True,
                    "message": "Authentication successful",
                    "user": safe_user,
                    "token": f"KEY-JWT-{random.randint(100000, 999999)}-SECURE"
                })
            else:
                self._send_json(401, {
                    "status": "ERROR",
                    "success": False,
                    "message": "Invalid username or password. Please check your credentials."
                })
            return

        # 2. USER REGISTRATION
        if parsed.path == "/api/register":
            name = body.get("name", "").strip()
            email = body.get("email", "").strip()
            username = body.get("username", "").strip().lower()
            password = body.get("password", "").strip()

            if not username or not password or not name:
                self._send_json(400, {"status": "ERROR", "message": "All fields are required."})
                return

            if username in USERS_DB:
                self._send_json(409, {"status": "ERROR", "message": "Username is already registered."})
                return

            new_id = f"CUST-{random.randint(10000,99999)}"
            new_user = {
                "id": new_id,
                "username": username,
                "passwords": [password],
                "name": name,
                "nameKh": name,
                "role": "Retail Customer",
                "roleKh": "អតិថិជនទូទៅ",
                "department": "Retail Banking",
                "departmentKh": "សេវាអតិថិជនទូទៅ",
                "email": email,
                "avatar": "".join([part[0] for part in name.split()[:2]]).upper() or "CU",
                "avatarBg": "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)",
                "accessLevel": "CUSTOMER",
                "badgeColor": "#3b82f6",
                "dashboardTheme": "customer"
            }
            USERS_DB[username] = new_user
            STATE["activeUser"] = new_user
            safe_user = {k: v for k, v in new_user.items() if k != "passwords"}
            self._send_json(201, {
                "status": "SUCCESS",
                "success": True,
                "message": "Registration successful",
                "user": safe_user,
                "token": f"KEY-JWT-{random.randint(100000, 999999)}-SECURE"
            })
            return

        # 3. FUNDS TRANSFER API
        if parsed.path == "/api/transfer":
            source_acc = body.get("sourceAccountId", "ACC-CHK-9812")
            destination = body.get("recipient", "").strip()
            amount = float(body.get("amount", 0))
            memo = body.get("memo", "KEY Funds Transfer")
            
            if amount <= 0:
                self._send_json(400, {"status": "ERROR", "message": "Transfer amount must be greater than 0."})
                return

            acc = next((a for a in STATE["accounts"] if a["accountId"] == source_acc), STATE["accounts"][0])
            if acc["availableBalance"] < amount:
                self._send_json(400, {"status": "ERROR", "message": "Insufficient funds in selected account."})
                return

            acc["availableBalance"] -= amount
            txn_id = f"TXN-{random.randint(10000, 99999)}"
            new_txn = {
                "transactionId": txn_id,
                "postedDate": "Just now",
                "postedDateKh": "ទើបតែធ្វើរួច",
                "merchant": f"Transfer to {destination}",
                "category": "Transfer",
                "categoryKh": "ការផ្ទេរប្រាក់",
                "amount": -amount,
                "status": "COMPLETED",
                "statusKh": "បានជោគជ័យ"
            }
            STATE["transactions"].insert(0, new_txn)

            self._send_json(200, {
                "status": "SUCCESS",
                "success": True,
                "message": "Transfer completed successfully",
                "transactionId": txn_id,
                "amount": amount,
                "remainingBalance": acc["availableBalance"],
                "recipient": destination,
                "memo": memo
            })
            return

        # 4. CARD FREEZE / UNFREEZE
        if parsed.path in ["/api/card/freeze", "/api/cards/freeze"]:
            action = body.get("action", "toggle")
            card = STATE["cards"][0]
            if action == "freeze":
                card["status"] = "FROZEN"
                card["statusKh"] = "បានបង្កក"
            elif action == "unfreeze":
                card["status"] = "ACTIVE"
                card["statusKh"] = "សកម្ម"
            else:
                card["status"] = "FROZEN" if card["status"] == "ACTIVE" else "ACTIVE"
                card["statusKh"] = "បានបង្កក" if card["status"] == "FROZEN" else "សកម្ម"

            self._send_json(200, {"status": "SUCCESS", "success": True, "card": card})
            return

        if parsed.path in ["/api/cards/unfreeze"]:
            otp = body.get("otp", "").strip()
            if otp in ["123456", "123 456"]:
                STATE["cards"][0]["status"] = "ACTIVE"
                STATE["cards"][0]["statusKh"] = "សកម្ម"
                self._send_json(200, {"status": "SUCCESS", "success": True, "card": STATE["cards"][0]})
            else:
                self._send_json(400, {"status": "ERROR", "success": False, "message": "Invalid OTP code."})
            return

        # 5. TRAVEL NOTICE API
        if parsed.path in ["/api/card/travel", "/api/cards/travel-notice"]:
            destination = body.get("destination", "Overseas").strip()
            dates = body.get("dates", "Next 30 Days").strip()
            card = STATE["cards"][0]
            card["travelNotice"] = f"{destination} ({dates})"
            self._send_json(200, {"status": "SUCCESS", "success": True, "travelNotice": card["travelNotice"]})
            return

        # 6. DISPUTE SUBMISSION API
        if parsed.path in ["/api/disputes/create", "/api/disputes"]:
            merchant = body.get("merchant", "Unknown Online Retailer - London UK")
            amount = float(body.get("amount", 329.99))
            reason = body.get("reason", "Suspected Unauthorized Transaction")
            case_id = f"DSP-2026-{random.randint(1000, 9999)}"

            new_dispute = {
                "caseId": case_id,
                "transactionId": body.get("transactionId", f"TXN-{random.randint(8000, 9999)}"),
                "merchant": merchant,
                "amount": amount,
                "currency": "$",
                "reason": reason,
                "reasonKh": reason,
                "status": "UNDER_INVESTIGATION",
                "statusKh": "កំពុងស៊ើបអង្កេត",
                "provisionalCredit": amount,
                "filedAt": datetime.now(timezone.utc).isoformat(),
                "provisionalCreditStatus": "PROVISIONALLY_CREDITED",
                "provisionalCreditStatusKh": "បានបញ្ចូលឥណទានបណ្តោះអាសន្ន"
            }
            STATE["disputes"].insert(0, new_dispute)
            STATE["cards"][0]["status"] = "FROZEN"
            STATE["cards"][0]["statusKh"] = "បានបង្កក"
            self._send_json(201, {"status": "SUCCESS", "success": True, "dispute": new_dispute})
            return

        # 7. CHANGE PASSWORD API
        if parsed.path == "/api/security/password":
            username = body.get("username", "").strip().lower()
            old_pwd = body.get("oldPassword", "").strip()
            new_pwd = body.get("newPassword", "").strip()

            user = USERS_DB.get(username)
            if not user or old_pwd not in user.get("passwords", []):
                self._send_json(400, {"status": "ERROR", "message": "Current password is incorrect."})
                return

            user["passwords"].append(new_pwd)
            self._send_json(200, {"status": "SUCCESS", "message": "Password updated successfully."})
            return

        # 8. COPILOT STUDIO DIRECT LINE CONFIGURATION API
        if parsed.path == "/api/copilot/config":
            secret = body.get("directLineSecret", "").strip()
            endpoint = body.get("tokenEndpoint", "").strip()
            if secret:
                COPILOT_STUDIO_CONFIG["directLineSecret"] = secret
            if endpoint:
                COPILOT_STUDIO_CONFIG["tokenEndpoint"] = endpoint
            COPILOT_STUDIO_CONFIG["lastTested"] = datetime.now(timezone.utc).isoformat()
            self._send_json(200, {
                "status": "SUCCESS",
                "message": "Copilot Studio Direct Line configuration updated",
                "directLineConfigured": bool(COPILOT_STUDIO_CONFIG["directLineSecret"])
            })
            return

        # 9. COPILOT CHAT (VICHHAI AI)
        if parsed.path == "/api/chat":
            user_msg = body.get("message", "")
            session_id = body.get("sessionId", "demo-session-1")
            lang = body.get("lang", "auto")
            username = body.get("username", body.get("user_id", "admin")).lower()
            user = USERS_DB.get(username, STATE["activeUser"] or USERS_DB["sophanith"])
            
            result = execute_agentic_reasoning(user_msg, session_id, lang, user)
            self._send_json(200, result)
            return

        self._send_json(404, {"error": "Not Found"})

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), DemoAppHandler)
    print(f"KEY Bank Enterprise Server running on http://0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server.")
        server.server_close()
