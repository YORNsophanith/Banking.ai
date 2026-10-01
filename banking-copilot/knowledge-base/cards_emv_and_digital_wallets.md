# KEY Bank — Payment Cards, EMV Security & Digital Wallets Knowledge Base

## 1. Card Portfolio & Specifications

### A. Visa Platinum Debit Card (កាតឥណពន្ធ វីសា ប្លាទីនីម)
- **Annual Card Fee:** $15.00 USD (Waived with minimum annual spend of $1,200).
- **Daily ATM Withdrawal Limit:** **$1,000.00 USD / 4,000,000 KHR per day** (Max $500 per single ATM withdrawal).
- **Daily Point-of-Sale (POS) & E-Commerce Limit:** **$5,000.00 USD / 20,000,000 KHR per day**.
- **Contactless (PayWave) Limit without PIN:** Up to $50.00 USD per transaction.
- **Foreign Currency Transaction Fee:** **1.50%** FX markup on international transactions outside Cambodia.

### B. Visa Platinum & Signature Credit Cards (កាតឥណទាន វីសា)
- **Credit Limit Range:** $2,000 to **$20,000 USD** (Platinum) | $20,000 to **$50,000 USD** (Signature).
- **Interest-Free Grace Period:** Up to **45 Days Interest-Free** for purchases settled in full by the monthly statement due date.
- **Annual Percentage Rate (Revolving APR):** **18.00% p.a.** (Calculated at 1.50% per month on unpaid balance).
- **Minimum Monthly Payment:** **5% of the total statement balance or $10.00 USD** (whichever is greater).
- **Cash Advance Fee:** 3.00% or minimum $5.00 USD per withdrawal.
- **Complimentary Benefits:**
  - Free International Travel Accident Insurance up to $500,000 USD when flight tickets are charged to the card.
  - Priority Pass Airport Lounge access (2 complimentary visits per year for Platinum; 6 visits for Signature).
  - 1% Cash Back on Dining and Supermarket grocery spend.

---

## 2. Card Security Controls & Self-Service Operations

### A. Instant Card Freeze / Lock (ចាក់សោរកាតភ្លាមៗ)
- **Trigger:** Immediate lock when card is misplaced, stolen, or suspicious activity is suspected.
- **Effects:** Instantly rejects all new POS authorization attempts, online e-commerce checkouts, and ATM cash withdrawals.
- **Pre-authorized Recurring Subscriptions:** Paused during freeze.
- **Execution:** Zero wait time, executed instantly via Vichhai AI or Web Portal.

### B. Step-Up 2FA Unfreeze Protocol (ដោះសោកាតដោយសុវត្ថិភាព)
- **Security Guardrail:** Card unfreezing is categorized as a High-Risk Privileged Operation.
- **Challenge:** Vichhai AI issues a **Time-Based One-Time Passcode (TOTP/SMS OTP)** sent to the registered mobile phone number (`+855 •• ••• 888`).
- **Demo Passcode:** `123456`
- **Validation:** Once verified, the card state is immediately flipped back to `ACTIVE`.

### C. Travel Notice Exemption (ការជូនដំណឹងធ្វើដំណើរទៅក្រៅប្រទេស)
- **Purpose:** Prevents automated fraud scoring engines from blocking international card authorizations when customers travel abroad.
- **Registration Parameters:** Destination Country (e.g., Japan, USA, France, Thailand, Singapore) + Travel Dates.
- **Execution:** Real-time synchronization with the Visa Cardholder Fraud Monitoring Engine.
