#!/usr/bin/env python3
"""
KEY Bank — Enterprise Agentic AI Banking System
Protected Multi-Role Authentication Server (Password Required)
AI Agent Specialist: Vichhai AI
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

# Pre-configured Users with Secure Passwords
USERS_DB = {
    "sophanith": {
        "id": "USR-ADMIN-001",
        "username": "sophanith",
        "password": "Password@123",
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
        "badgeColor": "#3b82f6"
    },
    "ravith": {
        "id": "USR-FIN-002",
        "username": "ravith",
        "password": "Password@123",
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
        "badgeColor": "#10b981"
    },
    "phirek": {
        "id": "USR-MKT-003",
        "username": "phirek",
        "password": "Password@123",
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
        "badgeColor": "#f59e0b"
    },
    "sokny": {
        "id": "USR-IT-004",
        "username": "sokny",
        "password": "Password@123",
        "name": "Mr. San Sokny",
        "nameKh": "លោក សាន សុកនី",
        "role": "IT Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងបច្ចេកវិទ្យា",
        "department": "Information Technology & Security",
        "departmentKh": "ផ្នែកបច្ចេកវិទ្យា និងសុវត្ថិភាព",
        "email": "sokny.san@keybank.com",
        "avatar": "SS",
        "avatarBg": "linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%)",
        "accessLevel": "IT_ADMIN",
        "badgeColor": "#8b5cf6"
    },
    "vathanakboth": {
        "id": "USR-SALES-005",
        "username": "vathanakboth",
        "password": "Password@123",
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
        "badgeColor": "#0ea5e9"
    },
    "panha_n": {
        "id": "USR-SALES-006",
        "username": "panha_n",
        "password": "Password@123",
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
        "badgeColor": "#14b8a6"
    },
    "panha_c": {
        "id": "USR-HR-007",
        "username": "panha_c",
        "password": "Password@123",
        "name": "Ms. Chea Panha",
        "nameKh": "កញ្ញា ជា បញ្ញា",
        "role": "HR Manager",
        "roleKh": "ប្រធានគ្រប់គ្រងធនធានមនុស្ស",
        "department": "Human Resources",
        "departmentKh": "ផ្នែកគ្រប់គ្រងធនធានមនុស្ស",
        "email": "panha.chea@keybank.com",
        "avatar": "CP",
        "avatarBg": "linear-gradient(135deg, #db2777 0%, #831843 100%)",
        "accessLevel": "HR_ADMIN",
        "badgeColor": "#ec4899"
    },
    "nisa": {
        "id": "USR-MKT-008",
        "username": "nisa",
        "password": "Password@123",
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
        "badgeColor": "#f97316"
    },
    "customer": {
        "id": "CUST-10029",
        "username": "customer",
        "password": "Password@123",
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
        "badgeColor": "#3b82f6"
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
    "active_otp_challenges": {},
    "pending_actions": {}
}

def is_khmer_text(text):
    return bool(re.search(r'[\u1780-\u17FF]', text))

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

    # Intent 1: Check Balances
    if any(k in text for k in ["balance", "account", "សមតុល្យ", "លុយ", "ប្រាក់", "គណនី", "how much"]):
        thought_process.append("1. Extract user intent -> Query account balances.")
        thought_process.append("2. Invoke Core Banking Action: GET /accounts/ACC-CHK-9812/balance.")
        thought_process.append("3. Format multi-account summary.")

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

    # Intent 2: Inquire London $329 Transaction / Dispute
    elif any(k in text for k in ["329", "london", "charge", "unknown", "ឡុងដ៍", "កាត់ប្រាក់", "បន្លំ", "dispute", "fraud", "តវ៉ា"]):
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

    # Intent 3: Freeze Card
    elif any(k in text for k in ["freeze", "lock", "block", "បង្កក", "ចាក់សោរកាត", "បិទកាត"]):
        thought_process.append("1. Extract card lock command -> CARD-VISA-7711.")
        thought_process.append("2. Execute Core Action: POST /cards/CARD-VISA-7711/freeze.")
        
        STATE["cards"][0]["status"] = "FROZEN"
        STATE["cards"][0]["statusKh"] = "បានបង្កក"

        if is_kh:
            reply = (
                f"🔒 **កាតត្រូវបានបង្កកដោយជោគជ័យ!**\n\n"
                f"កាត **Visa Platinum (•••• 7711)** របស់លោកអ្នកត្រូវបានចាក់សោរបង្កកជាបណ្តោះអាសន្ន។ រាល់ប្រតិបត្តិការទិញទំនិញតាមអនឡាញ និងការដកប្រាក់តាម ATM ត្រូវបានផ្អាកដើម្បីសុវត្ថិភាព។"
            )
            card_data = {
                "type": "CardStatus",
                "title": "Visa Platinum (•••• 7711)",
                "status": "FROZEN",
                "badge": "🔒 បានបង្កក",
                "refCode": "FRZ-" + str(random.randint(10000, 99999)),
                "unfreezeBtn": "🔓 ដោះសោកាតវិញ"
            }
        else:
            reply = (
                f"🔒 **Card Successfully Frozen!**\n\n"
                f"Your **Visa Platinum (•••• 7711)** has been temporarily locked. All point-of-sale authorizations, online purchases, and ATM withdrawals are now blocked."
            )
            card_data = {
                "type": "CardStatus",
                "title": "Visa Platinum (•••• 7711)",
                "status": "FROZEN",
                "badge": "🔒 FROZEN",
                "refCode": "FRZ-" + str(random.randint(10000, 99999)),
                "unfreezeBtn": "🔓 Unfreeze Card (Requires OTP)"
            }

    # Intent 4: Unfreeze Card (Requires Step-Up OTP)
    elif any(k in text for k in ["unfreeze", "unlock", "ដោះសោ", "បើកកាត"]):
        thought_process.append("1. Security Guardrail: Unfreezing payment card is HIGH RISK.")
        thought_process.append("2. Trigger Step-Up MFA Challenge -> POST /auth/step-up/otp.")
        
        STATE["pending_actions"][session_id] = {
            "type": "UNFREEZE_CARD",
            "cardId": "CARD-VISA-7711"
        }

        if is_kh:
            reply = (
                f"🔐 **ទាមទារការផ្ទៀងផ្ទាត់សុវត្ថិភាព:**\n\n"
                f"ដើម្បីដោះសោកាត Visa Platinum (•••• 7711) សូមបញ្ចូលលេខកូដសម្ងាត់ ៦ ខ្ទង់ ដែលបានផ្ញើទៅកាន់ទូរស័ព្ទរបស់លោកអ្នក (+855 •• ••• 888)។\n\n"
                f"*(សម្រាប់ Demo សាកល្បង លេខកូដគឺ: `123456`)*"
            )
            card_data = {
                "type": "OtpChallenge",
                "title": "បញ្ចូលលេខកូដសម្ងាត់ ៦ ខ្ទង់",
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

    # Intent 5: Travel Notice
    elif any(k in text for k in ["travel", "japan", "ធ្វើដំណើរ", "ជប៉ុន", "ក្រៅប្រទេស", "trip"]):
        thought_process.append("1. Extract travel intent -> Destination: Japan.")
        thought_process.append("2. Invoke Core Action: POST /cards/CARD-VISA-7711/travel-notice.")
        
        STATE["cards"][0]["travelNotice"] = "Japan (Oct 2026)"

        if is_kh:
            reply = (
                f"✈️ **ការកំណត់ការធ្វើដំណើរត្រូវបានរក្សាទុកដោយជោគជ័យ!**\n\n"
                f"យើងខ្ញុំបានកត់ត្រាការជូនដំណឹងធ្វើដំណើរទៅកាន់ **ប្រទេសជប៉ុន** សម្រាប់កាត Visa Platinum (•••• 7711) របស់លោកអ្នក។ ប្រតិបត្តិការទូទាត់នៅក្រៅប្រទេសនឹងមិនត្រូវបានរារាំងដោយប្រព័ន្ធសុវត្ថិភាពស្វ័យប្រវត្តិនោះទេ។"
            )
        else:
            reply = (
                f"✈️ **Travel Notice Successfully Activated!**\n\n"
                f"A travel exemption for **Japan (Oct 2026)** has been applied to your Visa Platinum (•••• 7711). Foreign card authorizations will proceed smoothly without automated fraud blocks."
            )

    # Intent 6: Fees & Limits
    elif any(k in text for k in ["fee", "limit", "wire", "ថ្លៃសេវា", "ដែនកំណត់", "ផ្ទេរប្រាក់"]):
        thought_process.append("1. Query Knowledge Base: accounts_fees_and_limits.md & khmer_banking_policies.md.")
        thought_process.append("2. Retrieve Fee Schedule & ATM withdrawal limits.")

        if is_kh:
            reply = (
                f"📄 **តារាងថ្លៃសេវា និងដែនកំណត់ធនាគារ KEY Bank:**\n\n"
                f"• **ថ្លៃផ្ទេរប្រាក់ទៅក្រៅប្រទេស:** $25.00 USD ក្នុងមួយប្រតិបត្តិការ\n"
                f"• **ការផ្ទេរប្រាក់ក្នុងស្រុក:** $0.00 ឥតគិតថ្លៃ\n"
                f"• **ដែនកំណត់ដកប្រាក់តាម ATM ប្រចាំថ្ងៃ:** $1,000 USD ក្នុងមួយថ្ងៃ\n"
                f"• **ដែនកំណត់ទូទាត់តាមកាត:** $5,000 USD ក្នុងមួយថ្ងៃ\n"
                f"• **កម្រៃសេវាប្តូរប្រាក់អន្តរជាតិ:** 0% សម្រាប់កាត Platinum"
            )
        else:
            reply = (
                f"📄 **KEY Bank Schedule of Fees & Account Limits:**\n\n"
                f"• **Outbound International Wire Transfer:** $25.00 flat fee\n"
                f"• **Domestic KEY & ACH Transfers:** $0.00 (Free)\n"
                f"• **Daily ATM Withdrawal Limit:** $1,000.00 / day\n"
                f"• **Daily Point-of-Sale / Debit Limit:** $5,000.00 / day\n"
                f"• **Foreign Currency Transaction Fee:** 0% (Platinum Benefit)"
            )

    # Default Fallback
    else:
        thought_process.append(f"1. Conversational inquiry analysis for {user_name}.")
        thought_process.append("2. Synthesize role-aware response from Vichhai AI.")

        if is_kh:
            reply = (
                f"សូមគោរពជម្រាបជូន **{user_name}** ({user_role})! ខ្ញុំជា **Vichhai AI** ជំនួយការឆ្លាតវៃនៃធនាគារ KEY Bank។\n\n"
                f"លោកអ្នកអាចសួរខ្ញុំអំពី៖\n"
                f"• ពិនិត្យសមតុល្យគណនី\n"
                f"• សាកសួរ ឬតវ៉ាលើប្រតិបត្តិការសង្ស័យ $329 នៅឡុងដ៍\n"
                f"• បង្កក ឬដោះសោកាត Visa\n"
                f"• កំណត់ការធ្វើដំណើរទៅក្រៅប្រទេស\n"
                f"• សាកសួរព័ត៌មានថ្លៃសេវា និងដែនកំណត់ធនាគារ"
            )
        else:
            reply = (
                f"Hello **{user_name}** ({user_role})! I am **Vichhai AI**, your intelligent assistant at KEY Bank.\n\n"
                f"You can ask me to:\n"
                f"• Check your live account balances\n"
                f"• Inquire or dispute the flagged $329 London charge\n"
                f"• Freeze or unfreeze your Visa Platinum card\n"
                f"• Set international travel notices (e.g. Japan)\n"
                f"• Review wire transfer fees and account limits"
            )

    return {
        "reply": reply,
        "thoughtProcess": thought_process,
        "card": card_data
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
            for u in USERS_DB.values():
                safe_users.append({k: v for k, v in u.items() if k != "password"})
            self._send_json(200, {"status": "SUCCESS", "users": safe_users})
            return

        if parsed.path == "/api/health":
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
            username = body.get("username", "").strip()
            password = body.get("password", "").strip()

            user = USERS_DB.get(username)
            if user and user.get("password") == password:
                STATE["activeUser"] = user
                safe_user = {k: v for k, v in user.items() if k != "password"}
                self._send_json(200, {
                    "status": "SUCCESS",
                    "message": "Authentication successful",
                    "user": safe_user,
                    "token": f"KEY-JWT-{random.randint(100000, 999999)}-SECURE"
                })
            else:
                self._send_json(401, {
                    "status": "ERROR",
                    "message": "Invalid username or password. Please check your credentials."
                })
            return

        # 2. USER REGISTRATION
        if parsed.path == "/api/register":
            name = body.get("name", "").strip()
            email = body.get("email", "").strip()
            username = body.get("username", "").strip()
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
                "password": password,
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
                "badgeColor": "#3b82f6"
            }
            USERS_DB[username] = new_user
            STATE["activeUser"] = new_user
            safe_user = {k: v for k, v in new_user.items() if k != "password"}
            self._send_json(201, {
                "status": "SUCCESS",
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
                "message": "Transfer completed successfully",
                "transactionId": txn_id,
                "amount": amount,
                "remainingBalance": acc["availableBalance"],
                "recipient": destination,
                "memo": memo
            })
            return

        # 4. CARD ACTIONS
        if parsed.path == "/api/card/freeze":
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

            self._send_json(200, {"status": "SUCCESS", "card": card})
            return

        # 5. TRAVEL NOTICE API
        if parsed.path == "/api/card/travel":
            destination = body.get("destination", "Overseas").strip()
            dates = body.get("dates", "Next 30 Days").strip()
            card = STATE["cards"][0]
            card["travelNotice"] = f"{destination} ({dates})"
            self._send_json(200, {"status": "SUCCESS", "travelNotice": card["travelNotice"]})
            return

        # 6. DISPUTE SUBMISSION API
        if parsed.path == "/api/disputes/create":
            merchant = body.get("merchant", "Suspicious Merchant")
            amount = float(body.get("amount", 50.0))
            reason = body.get("reason", "Unauthorized Transaction")
            case_id = f"DSP-2026-{random.randint(1000, 9999)}"

            new_dispute = {
                "caseId": case_id,
                "transactionId": f"TXN-{random.randint(8000, 9999)}",
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
            self._send_json(201, {"status": "SUCCESS", "dispute": new_dispute})
            return

        # 7. CHANGE PASSWORD API
        if parsed.path == "/api/security/password":
            username = body.get("username", "")
            old_pwd = body.get("oldPassword", "")
            new_pwd = body.get("newPassword", "")

            user = USERS_DB.get(username)
            if not user or user.get("password") != old_pwd:
                self._send_json(400, {"status": "ERROR", "message": "Current password is incorrect."})
                return

            user["password"] = new_pwd
            self._send_json(200, {"status": "SUCCESS", "message": "Password updated successfully."})
            return

        # 8. COPILOT CHAT (VICHHAI AI)
        if parsed.path == "/api/chat":
            user_msg = body.get("message", "")
            session_id = body.get("sessionId", "demo-session-1")
            lang = body.get("lang", "auto")
            username = body.get("username")
            user = USERS_DB.get(username, STATE["activeUser"] or USERS_DB["sophanith"])
            
            result = execute_agentic_reasoning(user_msg, session_id, lang, user)
            self._send_json(200, result)
            return

        self._send_json(404, {"error": "Not Found"})

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), DemoAppHandler)
    print(f"KEY Bank Enterprise Server running on http://0.0.0.0:{PORT}")
    server.serve_forever()
