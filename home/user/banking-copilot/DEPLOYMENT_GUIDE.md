# Microsoft Copilot Studio — Banking Agentic AI Implementation & Deployment Guide

This repository contains the complete enterprise starter kit for building an **Autonomous Agentic AI for Banking Customer Inquiries** with **Microsoft Copilot Studio**.

---

## 📁 Repository Structure

```
banking-copilot/
├── openapi/
│   └── banking-core-api.json         # OpenAPI 3.0 spec for Custom Connector / AI Plugins
├── copilot-instructions/
│   └── system-prompt.md              # System prompt, guardrails & orchestration instructions
├── adaptive-cards/
│   ├── account-balance-card.json     # Visual UI Card for Account Balances
│   ├── card-freeze-card.json         # Visual UI Card for Lost/Frozen Card
│   ├── recent-transactions-card.json # Visual UI Card for Transaction History
│   ├── otp-challenge-card.json       # Visual UI Card for Step-up Auth
│   └── dispute-submission-card.json  # Visual UI Card for Dispute Case confirmation
├── knowledge-base/
│   ├── dispute_policy_and_fraud.md   # RAG source for Reg E/Z dispute rules
│   ├── accounts_fees_and_limits.md   # RAG source for fee schedules & wire limits
│   └── cards_and_travel_notices.md   # RAG source for card management & travel notices
├── mock-api/
│   └── server.py                     # Local Core Banking mock API server (Port 8000)
└── tests/
    └── test_scenarios.py             # Validation test suite for banking API actions
```

---

## 🚀 Step-by-Step Deployment Instructions

### Phase 1: Import the Custom Connector into Power Platform

1. Navigate to [Power Apps Maker Portal](https://make.powerapps.com/) or [Copilot Studio Portal](https://copilotstudio.microsoft.com/).
2. Select your designated banking **Environment** (e.g., `UAT-Banking-Agent`).
3. Under **Custom Connectors** (or **Data > Custom Connectors**):
   - Click **+ New custom connector** $\rightarrow$ **Import an OpenAPI file**.
   - Connector Name: `CoreBankingServiceConnector`.
   - Upload file: `banking-copilot/openapi/banking-core-api.json`.
4. In the **General** tab:
   - Host: Enter your Azure API Management (APIM) URL or sandbox URL.
5. In the **Security** tab:
   - Authentication Type: `API Key` or `OAuth 2.0` (with Microsoft Entra ID).
6. Click **Create Connector**.

---

### Phase 2: Create the Agent in Microsoft Copilot Studio

1. Open [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/).
2. Click **+ Create an agent** (or **Create a copilot**).
3. Name: `Apex Premier Banking Assistant`.
4. Language: `English (US)` (or multi-lingual as needed).
5. **System Instructions**:
   - Go to **Settings > Overview > Instructions**.
   - Copy the complete system prompt from `banking-copilot/copilot-instructions/system-prompt.md` and paste it into the Instructions field.

---

### Phase 3: Ground the Agent with Knowledge Sources (RAG)

1. Navigate to the **Knowledge** tab in your agent.
2. Click **+ Add knowledge**.
3. Choose **Files**:
   - Upload the 3 files from `banking-copilot/knowledge-base/`:
     - `dispute_policy_and_fraud.md`
     - `accounts_fees_and_limits.md`
     - `cards_and_travel_notices.md`
4. Set **Search & Content Moderation**:
   - Under **Generative AI settings**, set the Moderation Level to **High** to ensure the model does not hallucinate beyond the provided documentation.

---

### Phase 4: Add Actions (AI Plugins / Dynamic Chaining)

1. In Copilot Studio, click the **Actions** tab $\rightarrow$ **+ Add an action**.
2. Select the `CoreBankingServiceConnector` connector created in Phase 1.
3. Enable the following registered operations:
   - `getCustomerAccounts`
   - `getAccountBalance`
   - `getRecentTransactions`
   - `updateCardStatus`
   - `createTransactionDispute`
   - `sendStepUpOtp`
   - `verifyStepUpOtp`
4. For each action:
   - Review parameter descriptions to ensure the LLM knows how to extract inputs from user context.
   - For high-impact actions (`updateCardStatus`, `createTransactionDispute`), toggle **Ask confirmation before running this action** to `ON`.

---

### Phase 5: Enable Generative Orchestration

1. In Copilot Studio, go to **Settings > Generative AI**.
2. Under **How should your copilot decide how to talk to people?**, select:
   - **Generative (Dynamic Chaining)**.
3. This allows the Agentic AI to:
   - Plan multi-turn action sequences automatically.
   - Combine knowledge lookups with API actions without hardcoding rigid decision trees.

---

### Phase 6: Rich Adaptive Card Formatting

To display formatted cards instead of plain text:
1. In Topics or Action response templates, insert an **Adaptive Card** node.
2. Paste the JSON template from the `banking-copilot/adaptive-cards/` folder corresponding to the action:
   - Balance check: `account-balance-card.json`
   - Card freeze: `card-freeze-card.json`
   - OTP input modal: `otp-challenge-card.json`
   - Dispute receipt: `dispute-submission-card.json`
3. Map the dynamic fields (e.g., `accountId`, `availableBalance`, `cardMasked`) to the variables returned by the Action.

---

### Phase 7: Live Human Escalation Configuration

1. In Copilot Studio, go to the **Topics** tab $\rightarrow$ **Escalate** (or **Transfer Conversation**).
2. Configure your live contact center destination:
   - **Microsoft Dynamics 365 Contact Center / Omnichannel for Customer Service**
   - **Genesys Cloud / NICE inContact / Twilio Flex**
3. In the transfer payload, bind:
   - `va_ConversationSummary`: AI auto-summary of the customer issue.
   - `va_CustomerRiskLevel`: Risk score (Low / Medium / Fraud).
   - `va_CustomerContext`: Customer ID and verified session tokens.

---

## 🧪 Local Testing & Verification

The mock server is pre-configured and running locally on port `8000`.

To run the full regression test suite:
```bash
python3 /home/user/banking-copilot/tests/test_scenarios.py
```

### Sample User Interaction Flow:
1. **User**: *"I think someone charged my card in London for $329. I didn't buy that!"*
2. **Copilot (RAG + Orchestration)**: 
   - Calls `getRecentTransactions` $\rightarrow$ identifies `TXN-9010` ($329.99 from Unknown Online Retailer - London UK).
   - Responds: *"I see a transaction on Sept 27 for $329.99 at Unknown Online Retailer. For your safety, I can freeze your Visa ending in 7711 and file a dispute case right away. Would you like me to freeze the card now?"*
3. **User**: *"Yes, please freeze it and file the dispute."*
4. **Copilot**:
   - Calls `updateCardStatus(cardId="CARD-VISA-7711", newStatus="FROZEN")`.
   - Calls `createTransactionDispute(...)` $\rightarrow$ returns case `DSP-2026-XXXXX`.
   - Displays the **Dispute Confirmation Adaptive Card** and notes provisional credit rules from the knowledge base.
