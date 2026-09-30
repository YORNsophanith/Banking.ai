#!/usr/bin/env python3
"""
Interactive Banking Agentic AI Demo Server (Bilingual: English + ភាសាខ្មែរ)
Provides a complete 100% FREE demonstration environment mimicking Microsoft Copilot Studio + Core Banking System.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import re
import urllib.parse
from datetime import datetime, timezone
import random

PORT = 3000
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
KB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge-base")

# Live Banking State (for demo dashboard sync)
STATE = {
    "customer": {
        "customerId": "CUST-10029",
        "customerName": "Alex Morgan",
        "email": "alex.morgan@example.com",
        "phone": "+1 (555) 019-8812",
        "memberTier": "Premier Platinum Member",
        "memberTierKh": "សមាជិកកម្រិតផ្លាទីនៀម (Premier Platinum)"
    },
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
            "merchant": "Direct Deposit - ACME Global Payroll",
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
    """Detect if the input string contains Khmer Unicode characters."""
    return bool(re.search(r'[\u1780-\u17FF]', text))

def execute_agentic_reasoning(user_text, session_id, lang_preference="auto"):
    """
    Simulates the Copilot Studio Generative Orchestrator with Agentic Dynamic Chaining
    with full support for both English and Khmer (ភាសាខ្មែរ).
    """
    text = user_text.lower().strip()
    is_kh = is_khmer_text(user_text) or lang_preference == "km"
    logs = []
    response_payload = {
        "reply": "",
        "thoughtProcess": [],
        "toolCalls": [],
        "card": None,
        "suggestedActions": []
    }

    # 1. Intent Recognition & Planning
    if is_kh:
        logs.append(f"🧠 ជំហានទី១ [ការវិភាគបំណង (Intent)]: ទទួលសារជាភាសាខ្មែរ: '{user_text}'")
    else:
        logs.append(f"🧠 Step 1 [Reasoning]: Analyzing intent for user utterance: '{user_text}'")

    # CASE: OTP Submission
    if "123456" in text or re.search(r"\b\d{6}\b", text):
        otp_match = re.search(r"\b\d{6}\b", text).group(0)
        logs.append(f"🔧 Step 2 [Tool Call]: verifyStepUpOtp(challengeId='active', otpCode='{otp_match}')")
        
        if otp_match == "123456":
            logs.append("✅ Step 3 [Tool Result]: Step-up authentication SUCCESS (VerificationToken generated).")
            pending = STATE["pending_actions"].get(session_id)
            if pending and pending.get("type") == "UNFREEZE":
                STATE["cards"][0]["status"] = "ACTIVE"
                STATE["cards"][0]["statusKh"] = "សកម្ម (ACTIVE)"
                logs.append("🔧 Step 4 [Tool Call]: updateCardStatus(cardId='CARD-VISA-7711', newStatus='ACTIVE')")
                
                if is_kh:
                    response_payload["reply"] = "✅ **ការផ្ទៀងផ្ទាត់អត្តសញ្ញាណបានជោគជ័យ!** កាត Visa លេខចុងក្រោយ **7711** របស់អ្នកត្រូវបាន **ដោះសោ (UNFROZEN)** រួចរាល់ហើយ និងអាចប្រើប្រាស់ទូទាត់ប្រាក់បានភ្លាមៗ។"
                    response_payload["card"] = {
                        "type": "StatusUpdate",
                        "title": "កាតត្រូវបានដោះសោ និងមានសុពលភាព",
                        "badge": "សកម្ម (ACTIVE)",
                        "badgeColor": "green",
                        "details": [
                            {"label": "កាត", "val": "Visa Platinum (•••• 7711)"},
                            {"label": "ស្ថានភាព", "val": "សកម្ម (អាចប្រើប្រាស់បាន)"},
                            {"label": "វិធីសាស្ត្រផ្ទៀងផ្ទាត់", "val": "Two-Factor Step-Up OTP"}
                        ]
                    }
                else:
                    response_payload["reply"] = "✅ **Identity Verified!** Your Visa card ending in **7711** has been successfully **UNFROZEN** and is active for purchases immediately."
                    response_payload["card"] = {
                        "type": "StatusUpdate",
                        "title": "Card Unfrozen & Active",
                        "badge": "ACTIVE",
                        "badgeColor": "green",
                        "details": [
                            {"label": "Card", "val": "Visa Platinum (•••• 7711)"},
                            {"label": "Status", "val": "ACTIVE (Ready to use)"},
                            {"label": "Auth Method", "val": "Two-Factor Step-Up OTP"}
                        ]
                    }
            else:
                if is_kh:
                    response_payload["reply"] = "✅ **ការផ្ទៀងផ្ទាត់បានជោគជ័យ!** តើខ្ញុំអាចជួយអ្វីបន្ថែមលើគណនីរបស់អ្នកនៅថ្ងៃនេះ?"
                else:
                    response_payload["reply"] = "✅ **Identity Verified!** Step-up authentication succeeded. How can I assist you with your account today?"
        else:
            logs.append("❌ Step 3 [Tool Result]: Step-up authentication FAILED (Invalid OTP).")
            if is_kh:
                response_payload["reply"] = "⚠️ លេខកូដសម្ងាត់មិនត្រឹមត្រូវ ឬផុតកំណត់។ សម្រាប់ demo សូមវាយបញ្ចូល: **123456**។"
            else:
                response_payload["reply"] = "⚠️ The passcode entered is invalid or expired. For demo testing, please enter **123456**."
        
        response_payload["thoughtProcess"] = logs
        return response_payload

    # CASE: Card Freeze / Unfreeze
    is_freeze_query = any(k in text for k in ["freeze", "lock", "lost my card", "stolen", "misplaced", "block card", "បង្កក", "បិទកាត", "បាត់កាត", "ចាក់សោ", "លួច", "លួចកាត"])
    is_unfreeze_query = any(k in text for k in ["unfreeze", "unlock", "ដោះសោ", "បើកកាត", "ដោះបង្កក", "ឈប់បង្កក"])

    if is_unfreeze_query:
        logs.append("🔐 Step 2 [Security Rule]: Unfreezing card is a High-Risk operation. Triggering Step-Up OTP challenge.")
        logs.append("🔧 Step 3 [Tool Call]: sendStepUpOtp(customerId='CUST-10029', action='CARD_UNFREEZE')")
        STATE["pending_actions"][session_id] = {"type": "UNFREEZE"}
        
        if is_kh:
            response_payload["reply"] = "🔒 ដើម្បីដោះសោកាតរបស់អ្នក សូមបញ្ចូលលេខកូដសម្ងាត់ ៦ ខ្ទង់ (OTP) ដែលបានផ្ញើទៅលេខទូរស័ព្ទ **+1 (***) ***-8812** របស់អ្នក។\n\n*(💡 សម្រាប់ការសាកល្បង Demo: សូមវាយបញ្ចូលលេខ **123456**)*"
            response_payload["card"] = {
                "type": "OtpChallenge",
                "title": "តម្រូវឱ្យផ្ទៀងផ្ទាត់សុវត្ថិភាព (OTP)",
                "phone": "+1 (***) ***-8812",
                "action": "UNFREEZE_CARD",
                "btnText": "បញ្ចូលលេខកូដ: 123456"
            }
        else:
            response_payload["reply"] = "🔒 To unfreeze your card, please enter the 6-digit security code sent to your registered phone **+1 (***) ***-8812**.\n\n*(💡 Demo tip: Type **123456** to verify)*"
            response_payload["card"] = {
                "type": "OtpChallenge",
                "title": "Security Verification Required",
                "phone": "+1 (***) ***-8812",
                "action": "UNFREEZE_CARD",
                "btnText": "Enter Code: 123456"
            }
        response_payload["thoughtProcess"] = logs
        return response_payload

    if is_freeze_query:
        logs.append("🧠 Step 2 [Plan]: User requested card freeze. Evaluating current card status.")
        STATE["cards"][0]["status"] = "FROZEN"
        STATE["cards"][0]["statusKh"] = "បានបង្កក (FROZEN)"
        ref = f"CONF-{random.randint(1000, 9999)}-FRZ"
        logs.append(f"🔧 Step 3 [Tool Call]: updateCardStatus(cardId='CARD-VISA-7711', newStatus='FROZEN', reason='Customer request') -> Reference: {ref}")
        
        if is_kh:
            response_payload["reply"] = f"🛡️ **កាត Visa របស់អ្នកត្រូវបាន បង្កក (FROZEN) ជាបណ្តោះអាសន្នភ្លាមៗ!**\n\nរាល់ការទូទាត់ទិញទំនិញថ្មីៗ ការទូទាត់អនឡាញ និងការដកប្រាក់តាមទូ ATM ត្រូវបានផ្អាកដើម្បីសុវត្ថិភាព។ ប៉ុន្តែការទូទាត់វិក្កយបត្រដែលបានកំណត់ស្វ័យប្រវត្តិនឹងដំណើរការធម្មតា។\n\n*លេខកូដយោងសុវត្ថិភាព: `{ref}`*"
            response_payload["card"] = {
                "type": "CardStatus",
                "title": "កាតត្រូវបានបង្កកជាបណ្តោះអាសន្ន",
                "badge": "បានបង្កក (FROZEN)",
                "badgeColor": "red",
                "cardName": "Visa Platinum (•••• 7711)",
                "refCode": ref,
                "canUnfreeze": True,
                "unfreezeBtn": "🔓 ស្នើសុំដោះសោកាតវិញ (ត្រូវការ OTP)"
            }
            response_payload["suggestedActions"] = ["ដោះសោកាតវិញ", "ពិនិត្យប្រតិបត្តិការថ្មីៗ", "ដាក់ពាក្យតវ៉ាលើការកាត់ប្រាក់"]
        else:
            response_payload["reply"] = f"🛡️ **Your card has been FROZEN immediately.**\n\nAll new retail charges, online checkouts, and ATM withdrawals are blocked. Pre-authorized recurring bills will continue to process normally.\n\n*Reference Code: `{ref}`*"
            response_payload["card"] = {
                "type": "CardStatus",
                "title": "Card Temporarily Frozen",
                "badge": "FROZEN",
                "badgeColor": "red",
                "cardName": "Visa Platinum (•••• 7711)",
                "refCode": ref,
                "canUnfreeze": True,
                "unfreezeBtn": "🔓 Unfreeze Card (Requires OTP)"
            }
            response_payload["suggestedActions"] = ["Unfreeze Card", "Review Recent Charges", "File a Dispute"]

        response_payload["thoughtProcess"] = logs
        return response_payload

    # CASE: Dispute or Unrecognized London Charge ($329)
    if any(k in text for k in ["dispute", "unrecognized", "charge", "london", "fraud", "didn't buy", "didn't authorize", "329", "unknown retailer", "៣២៩", "ឡុងដ៍", "តវ៉ា", "មិនស្គាល់", "កាត់លុយ", "ក្លែងបន្លំ"]):
        logs.append("🧠 Step 2 [Plan]: Customer questioning transaction. Querying recent account transactions.")
        logs.append("🔧 Step 3 [Tool Call]: getRecentTransactions(accountId='ACC-CHK-9812', limit=5)")
        flagged_txn = STATE["transactions"][2]
        logs.append(f"🔍 Step 4 [Entity Match]: Identified suspect transaction '{flagged_txn['merchant']}' for ${abs(flagged_txn['amount'])}")

        if any(k in text for k in ["file", "yes", "confirm", "submit", "បាទ", "ចាស", "យល់ព្រម", "ដាក់ពាក្យ", "តវ៉ា"]):
            case_id = f"DSP-2026-{random.randint(10000, 99999)}"
            STATE["disputes"].append({"caseId": case_id, "txnId": flagged_txn["transactionId"], "amount": flagged_txn["amount"]})
            logs.append(f"🔧 Step 5 [Tool Call]: createTransactionDispute(customerId='CUST-10029', transactionId='{flagged_txn['transactionId']}', reason='UNRECOGNIZED_MERCHANT')")
            logs.append(f"📚 Step 6 [RAG Lookup]: Grounding response with 'khmer_banking_policies.md' (Regulation E clause)")

            if is_kh:
                response_payload["reply"] = f"✅ **ពាក្យបណ្តឹងតវ៉ាត្រូវបានបញ្ជូនដោយជោគជ័យ!**\n\n• **លេខកូដសំណុំរឿង (Case ID)**: `{case_id}`\n• **ប្រតិបត្តិការ**: {flagged_txn['merchant']} (${abs(flagged_txn['amount'])})\n• **ឥណទានបណ្តោះអាសន្ន**: ធនាគារនឹងផ្តល់ប្រាក់បណ្តោះអាសន្នចូលគណនីរបស់អ្នកវិញក្នុងរយៈពេល ៤៨ ម៉ោង ប្រសិនបើការស៊ើបអង្កេតលើសពី ១០ ថ្ងៃនៃថ្ងៃធ្វើការ។\n• **ស្ថានភាព**: កំពុងស្ថិតក្រោមការត្រួតពិនិត្យដោយផ្នែកសុវត្ថិភាព និងការក្លែងបន្លំ។"
                response_payload["card"] = {
                    "type": "DisputeReceipt",
                    "caseId": case_id,
                    "merchant": flagged_txn["merchant"],
                    "amount": f"${abs(flagged_txn['amount']):.2f}",
                    "status": "កំពុងត្រួតពិនិត្យ (UNDER REVIEW)",
                    "eta": "១០ ថ្ងៃនៃថ្ងៃធ្វើការ"
                }
                response_payload["suggestedActions"] = ["បង្កកកាត Visa ផងដែរ", "ពិនិត្យសមតុល្យគណនី", "ត្រឡប់ទៅម៉ឺនុយដើម"]
            else:
                response_payload["reply"] = f"✅ **Dispute Case Filed Successfully!**\n\n• **Case Reference**: `{case_id}`\n• **Transaction**: {flagged_txn['merchant']} (${abs(flagged_txn['amount'])})\n• **Provisional Credit**: Under Regulation E, a provisional credit will be credited to your checking account within 48 business hours if research exceeds 10 days.\n• **Status**: Under Review by Priority Fraud Team."
                response_payload["card"] = {
                    "type": "DisputeReceipt",
                    "caseId": case_id,
                    "merchant": flagged_txn["merchant"],
                    "amount": f"${abs(flagged_txn['amount']):.2f}",
                    "status": "UNDER_REVIEW",
                    "eta": "10 Business Days"
                }
                response_payload["suggestedActions"] = ["Freeze my card as well", "Check account balance", "View all transactions"]
        else:
            if is_kh:
                response_payload["reply"] = f"ខ្ញុំបានរកឃើញប្រតិបត្តិការដែលអ្នកកំពុងសាកសួរ:\n\n• **ឈ្មោះហាង/ក្រុមហ៊ុន**: {flagged_txn['merchant']}\n• **ចំនួនទឹកប្រាក់**: **${abs(flagged_txn['amount']):.2f}**\n• **កាលបរិច្ឆេទ**: {flagged_txn['postedDateKh']}\n\nតើអ្នកចង់ឱ្យខ្ញុំ **ដាក់ពាក្យបណ្តឹងតវ៉ាជាផ្លូវការ** និង **បង្កកកាត Visa ជាបណ្តោះអាសន្ន** ដើម្បីការពារសុវត្ថិភាពដែរឬទេ?"
                response_payload["card"] = {
                    "type": "TransactionHighlight",
                    "merchant": flagged_txn["merchant"],
                    "amount": f"${abs(flagged_txn['amount']):.2f}",
                    "category": flagged_txn["categoryKh"],
                    "date": flagged_txn["postedDateKh"],
                    "actions": ["បាទ/ចាស ដាក់ពាក្យតវ៉ា និងបង្កកកាត", "គ្រាន់តែដាក់ពាក្យតវ៉ា", "ទេ ប្រតិបត្តិការនេះត្រឹមត្រូវ"]
                }
                response_payload["suggestedActions"] = ["បាទ ដាក់ពាក្យតវ៉ា និងបង្កកកាត", "បង្កកកាតតែមួយមុខ", "ម៉ឺនុយដើម"]
            else:
                response_payload["reply"] = f"I found the transaction you're referring to:\n\n• **Merchant**: {flagged_txn['merchant']}\n• **Amount**: **${abs(flagged_txn['amount']):.2f}**\n• **Date**: {flagged_txn['postedDate']}\n\nWould you like me to **file an official dispute case** and **temporarily freeze your Visa card** to prevent any further charges?"
                response_payload["card"] = {
                    "type": "TransactionHighlight",
                    "merchant": flagged_txn["merchant"],
                    "amount": f"${abs(flagged_txn['amount']):.2f}",
                    "category": flagged_txn["category"],
                    "date": flagged_txn["postedDate"],
                    "actions": ["Yes, File Dispute & Freeze Card", "Just File Dispute", "No, charge is okay"]
                }
                response_payload["suggestedActions"] = ["Yes, File Dispute & Freeze Card", "Freeze Card Only", "Main Menu"]

        response_payload["thoughtProcess"] = logs
        return response_payload

    # CASE: Balance Inquiry
    if any(k in text for k in ["balance", "how much money", "funds", "checking", "savings", "account balance", "សមតុល្យ", "លុយ", "គណនី", "ប្រាក់", "ប៉ុន្មាន"]):
        logs.append("🧠 Step 2 [Plan]: Balance inquiry detected. Retrieving all customer accounts.")
        logs.append("🔧 Step 3 [Tool Call]: getCustomerAccounts(customerId='CUST-10029')")
        chk = STATE["accounts"][0]
        sav = STATE["accounts"][1]

        if is_kh:
            response_payload["reply"] = f"នេះជាសេចក្តីសង្ខេបសមតុល្យគណនីសម្រាប់ **{STATE['customer']['memberTierKh']}** របស់អ្នក:\n\n• **គណនីចរន្តទូទៅ (Everyday Checking)** (`...9812`): **${chk['availableBalance']:,.2f}**\n• **គណនីសន្សំការប្រាក់ខ្ពស់ (High-Yield Savings)** (`...4109`): **${sav['availableBalance']:,.2f}**\n\n*ទ្រព្យសរុបដែលអាចប្រើប្រាស់បាន: **${(chk['availableBalance'] + sav['availableBalance']):,.2f}***"
            response_payload["suggestedActions"] = ["មើលប្រតិបត្តិការថ្មីៗ", "បង្កកកាត Visa", "សួរពីថ្លៃសេវាផ្ទេរប្រាក់"]
        else:
            response_payload["reply"] = f"Here is the real-time summary for your **{STATE['customer']['memberTier']}** accounts:\n\n• **Everyday Checking** (`...9812`): **${chk['availableBalance']:,.2f}**\n• **High-Yield Savings** (`...4109`): **${sav['availableBalance']:,.2f}**\n\n*Combined Liquid Assets: **${(chk['availableBalance'] + sav['availableBalance']):,.2f}***"
            response_payload["suggestedActions"] = ["View Recent Transactions", "Freeze Debit Card", "Wire Transfer Info"]
            
        response_payload["thoughtProcess"] = logs
        return response_payload

    # CASE: Travel Notice
    if any(k in text for k in ["travel", "japan", "europe", "trip", "overseas", "abroad", "vacation", "ជប៉ុន", "ដើរលេង", "ធ្វើដំណើរ", "ក្រៅប្រទេស"]):
        country = "ប្រទេសជប៉ុន (Japan)" if ("japan" in text or "ជប៉ុន" in text) else "តំបន់អឺរ៉ុប (Europe)" if ("europe" in text or "អឺរ៉ុប" in text) else "អន្តរជាតិ (International)"
        STATE["cards"][0]["travelNotice"] = f"{country} (Oct 1 - Oct 15, 2026)"
        logs.append(f"🔧 Step 3 [Tool Call]: setCardTravelNotice(cardId='CARD-VISA-7711', destination='{country}', duration='14 days')")
        logs.append("📚 Step 4 [RAG Lookup]: Grounding with 'khmer_banking_policies.md'")

        if is_kh:
            response_payload["reply"] = f"✈️ **ការជូនដំណឹងធ្វើដំណើរទៅកាន់ {country} ត្រូវបានកំណត់រួចរាល់!**\n\nប្រព័ន្ធសុវត្ថិភាពធនាគារនឹងទទួលស្គាល់ប្រតិបត្តិការស្របច្បាប់របស់អ្នកនៅ **{country}** ដោយមិនមានការរារាំង ឬបដិសេធឡើយ។\n\n• **រយៈពេល**: ១៤ ថ្ងៃបន្ទាប់\n• **លេខទូរស័ព្ទជំនួយបន្ទាន់ ២៤/៧**: +1 (800) 555-0199\n• **Apple Pay / Google Wallet**: ដំណើរការជាធម្មតានៅទូទាំងពិភពលោក។"
            response_payload["suggestedActions"] = ["ថ្លៃសេវាប្តូរប្រាក់បរទេស", "ដែនកំណត់ដកប្រាក់ ATM", "ត្រឡប់ទៅម៉ឺនុយដើម"]
        else:
            response_payload["reply"] = f"✈️ **Travel Notice Active for {country}!**\n\nI have updated your Visa Platinum ending in **7711**. Automated fraud neural filters will recognize legitimate transactions in **{country}** without declines.\n\n• **Dates**: Next 14 days\n• **Emergency Assistance**: 24/7 Global Collect: +1 (800) 555-0199\n• **Apple Pay / Google Wallet**: Remains active globally."
            response_payload["suggestedActions"] = ["Foreign Transaction Fee Info", "Check Daily ATM Limit", "Return to Menu"]

        response_payload["thoughtProcess"] = logs
        return response_payload

    # CASE: Fee schedule & Knowledge Base Questions (RAG)
    if any(k in text for k in ["fee", "wire", "atm limit", "overdraft", "policy", "cost", "ថ្លៃសេវា", "ផ្ទេរប្រាក់", "wire", "atm", "កាត់ថ្លៃ", "ថ្លៃ"]):
        logs.append("📚 Step 2 [RAG Semantic Search]: Querying knowledge index 'khmer_banking_policies.md'...")
        logs.append("📖 Step 3 [Grounding]: Found authoritative sections: Domestic Wire ($25), International Wire ($45), ATM Limit ($2,500).")
        
        if is_kh:
            response_payload["reply"] = "នេះជាតារាងថ្លៃសេវា និងដែនកំណត់ផ្លូវការសម្រាប់ **គណនី Premier Platinum** របស់អ្នក:\n\n• **ថ្លៃផ្ទេរប្រាក់ក្នុងស្រុក (Domestic Wire)**: **២៥.០០ ដុល្លារ**\n• **ថ្លៃផ្ទេរប្រាក់ទៅក្រៅប្រទេស (International Wire)**: **៤៥.០០ ដុល្លារ**\n• **ដែនកំណត់ដកប្រាក់ ATM ប្រចាំថ្ងៃ**: **២,៥០០.០០ ដុល្លារ** / ថ្ងៃ\n• **ដែនកំណត់ទិញទំនិញ POS ប្រចាំថ្ងៃ**: **១០,០០០.០០ ដុល្លារ** / ថ្ងៃ\n• **ថ្លៃដកប្រាក់តាម ATM ក្រៅបណ្តាញ**: **០.០០ ដុល្លារ** (សងត្រឡប់ជូនវិញដោយឥតគិតថ្លៃ)\n• **ថ្លៃថែទាំគណនីប្រចាំខែ**: **០.០០ ដុល្លារ** (មិនគិតថ្លៃ)។"
            response_payload["suggestedActions"] = ["ស្នើសុំបង្កើនដែនកំណត់បណ្តោះអាសន្ន", "ពិនិត្យសមតុល្យគណនី", "ជជែកជាមួយបុគ្គលិកផ្ទាល់"]
        else:
            response_payload["reply"] = "Here is the official fee and limits schedule for your **Premier Platinum Checking**:\n\n• **Domestic Wire Transfer**: **$25.00**\n• **International Wire Transfer**: **$45.00**\n• **Daily ATM Cash Limit**: **$2,500.00** per day\n• **Daily POS Debit Purchase Limit**: **$10,000.00** per day\n• **Out-of-Network ATM Surcharge**: **$0.00** *(Rebated at cycle end for Platinum members)*\n• **Monthly Maintenance Fee**: **$0.00** (Waived)."
            response_payload["suggestedActions"] = ["Request Temporary Limit Increase", "Check Balance", "Speak to Human Agent"]

        response_payload["thoughtProcess"] = logs
        return response_payload

    # DEFAULT / FALLBACK
    if is_kh:
        logs.append("🧠 Step 2 [Generative LLM]: Synthesizing general financial response in Khmer.")
        response_payload["reply"] = f"សួស្តី Alex! ខ្ញុំជា **ភ្នាក់ងារ AI ស្វ័យប្រវត្តិនៃធនាគារ Apex**។ ខ្ញុំអាចជួយអ្នកដោយសុវត្ថិភាពលើសេវាកម្មដូចខាងក្រោម:\n\n• 💳 **ពិនិត្យសមតុល្យគណនី និងរបាយការណ៍** (`គណនីចរន្ត និងសន្សំ`)\n• 🔍 **សាកសួរប្រតិបត្តិការ និងដាក់ពាក្យតវ៉ាលើការក្លែងបន្លំ**\n• 🔒 **បង្កកកាតភ្លាមៗ ឬដោះសោកាត Visa**\n• ✈️ **កំណត់ការជូនដំណឹងពេលធ្វើដំណើរទៅក្រៅប្រទេស**\n• 📄 **តារាងថ្លៃសេវាធនាគារ និងដែនកំណត់ប្រតិបត្តិការ**\n\nតើខ្ញុំអាចជួយអ្វីដល់អ្នកនៅថ្ងៃនេះ?"
        response_payload["suggestedActions"] = [
            "ពិនិត្យសមតុល្យគណនី",
            "ហេតុអ្វីមានការកាត់ប្រាក់ ៣២៩ ដុល្លារនៅឡុងដ៍?",
            "បង្កកកាត Visa របស់ខ្ញុំ",
            "កំណត់ការធ្វើដំណើរទៅប្រទេសជប៉ុន",
            "តើថ្លៃផ្ទេរប្រាក់ទៅក្រៅប្រទេសប៉ុន្មាន?"
        ]
    else:
        logs.append("🧠 Step 2 [Generative LLM]: Synthesizing general financial inquiry response grounded in Bank Service Handbook.")
        response_payload["reply"] = f"Hello Alex! I am your **Autonomous Banking Assistant**. I can securely help you with:\n\n• 💳 **Account Balances & Statements** (`Checking & Savings`)\n• 🔍 **Transaction Inquiries & Fraud Disputes**\n• 🔒 **Instant Card Freeze / Unfreeze Controls**\n• ✈️ **International Travel Notices**\n• 📄 **Fee Schedules, ATM Limits & Product Rates**\n\nHow can I help you today?"
        response_payload["suggestedActions"] = [
            "Check my balances",
            "Why was I charged $329 in London?",
            "Freeze my Visa card",
            "Set travel notice for Japan",
            "What are wire transfer fees?"
        ]

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
        if parsed.path == "/api/chat":
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length).decode('utf-8')) if length > 0 else {}
            user_msg = body.get("message", "")
            session_id = body.get("sessionId", "demo-session-1")
            lang = body.get("lang", "auto")
            
            result = execute_agentic_reasoning(user_msg, session_id, lang)
            self._send_json(200, result)
            return
        self._send_json(404, {"error": "Not Found"})

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), DemoAppHandler)
    print(f"Interactive Bilingual (EN + KM) Banking AI Demo Web App running on http://0.0.0.0:{PORT}")
    server.serve_forever()
