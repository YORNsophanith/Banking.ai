# KEY Bank — Fraud Prevention, Regulation E Disputes & AML/CFT Compliance

## 1. Consumer Protection & Dispute Resolution (Regulation E)

### A. Customer Dispute Rights & Reporting Timelines
- **Notification Period:** Cardholders have up to **60 calendar days** from the date the periodic statement is generated to report unauthorized or incorrect electronic fund transfers.
- **Common Dispute Categories:**
  1. **Fraud / Unauthorized Transaction (Reason Code 10.4):** Account debited without cardholder consent.
  2. **Merchandise/Services Not Received (Reason Code 13.1):** Paid goods not delivered by merchant.
  3. **Duplicate Charge / Incorrect Amount (Reason Code 12.5):** Charged multiple times for a single checkout.
  4. **Canceled Recurring Subscription (Reason Code 13.7):** Billed after explicit subscription cancellation.

### B. Provisional Credit SLA & Investigation Timeline
- **Provisional Credit Guarantee:** Under Regulation E and KEY Bank customer protection guidelines, if a dispute investigation cannot be resolved within **10 business days**, KEY Bank will issue a **100% Provisional Credit** directly to the customer's checking or savings account.
- **Investigation Timeframe:**
  - Standard domestic transactions: Resolved within **45 calendar days**.
  - Cross-border / Point-of-Sale foreign transactions: Extended up to **90 calendar days**.
- **Automated Card Safeguard:** When an unauthorized foreign dispute is filed (such as the $329.99 London charge), Vichhai AI automatically freezes the compromised card to block further fraudulent attempts.

---

## 2. AML/CFT Regulatory Framework & PII Privacy

### A. Anti-Money Laundering & Counter-Terrorist Financing (AML/CFT)
- **Cash Transaction Reporting (CTR):**
  - Any single cash deposit or withdrawal exceeding **$10,000 USD** (or **40,000,000 KHR**) triggers an automatic CTR filing with the Cambodia Financial Intelligence Unit (CAFIU).
  - Source of wealth documentation is required for cash transactions exceeding $50,000 USD.
- **Suspicious Transaction Reporting (STR):**
  - Transactions displaying rapid layering, structuring below the $10,000 threshold, or high-risk offshore counterparties are routed directly to the AML Compliance Department.

### B. Customer PII Tokenization & Privacy Masking Guardrails
- **Card Numbers (PAN):** Always masked showing only the last 4 digits (e.g., `•••• •••• •••• 7711`).
- **Account Numbers:** Masked showing only the last 4 digits (e.g., `******9812`).
- **Forbidden Credentials:** Vichhai AI and customer service agents are strictly prohibited from asking for or displaying CVV/CVC codes, PINs, or online banking passwords.
