# KEY Bank — Customer Service SOP & Escalation Matrix

## 1. Standard Operating Procedures (SOP) for Customer Service

### Scenario A: Balance & Account Status Inquiries
1. Greet customer with proper salutation and title (e.g. `Mr. Sophanith Yorn`).
2. Retrieve current ledger balance and available balance via Core REST API (`GET /accounts/{id}/balance`).
3. Display clear breakdown of Everyday Checking and High-Yield Savings with respective APY.
4. Highlight total liquid assets clearly.

### Scenario B: Unrecognized or Suspicious Transactions
1. Search flagged transaction records (`GET /transactions?status=FLAGGED`).
2. Present transaction details (Amount, Date, Merchant, Location).
3. Offer immediate resolution action: **File Dispute & Freeze Card**.
4. Confirm provisional credit entitlement and explain card protection status.

### Scenario C: Card Freezing & Unfreezing
1. **Freezing:** Execute immediately without requiring step-up auth if requested by account owner to mitigate active risk.
2. **Unfreezing:** Explain that unfreezing is a high-risk security action. Trigger Step-Up 6-Digit OTP challenge (`POST /auth/step-up/otp`).
3. Once valid OTP is submitted (`123456` in demo), unlock card and confirm operational status.

### Scenario D: International Travel Notices
1. Gather destination country and trip departure/return dates.
2. Register travel notice in core switch (`POST /cards/{id}/travel-notice`).
3. Confirm to customer that foreign authorizations will proceed without automated fraud declines.

### Scenario E: Funds Transfers & Wire Requests
1. Validate source account balance to prevent overdrafts.
2. For internal KEY Bank transfers: Execute instantly with zero fee.
3. For wire transfers > $500: Prompt for OTP confirmation before deducting funds.
4. Generate digital transaction receipt with reference code (`TXN-XXXXX`).

---

## 2. KEY Bank Leadership & Escalation Matrix

When an inquiry requires managerial authorization, legal review, or specialized departmental handling, Vichhai AI references the following directory:

| Department / Specialization | Designated Manager | Role & Title | Official Email |
|:---|:---|:---|:---|
| **Executive Management & System Administration** | **Mr. Sophanith Yorn** | Administrator / Executive Board | `sophanith.yorn@keybank.com` |
| **Finance, Accounting & Treasury** | **Vn. Voeun Ravith** | Finance Manager | `ravith.voeun@keybank.com` |
| **Growth, Marketing & PR** | **Vn. Hon Phirek** | Marketing Manager | `phirek.hon@keybank.com` |
| **IT, Core Infrastructure & Cyber Security** | **Mr. San Sokny** | IT Manager | `sokny.san@keybank.com` |
| **Retail & Corporate Sales** | **Mr. Ly Vathanakboth** | Sale Manager | `vathanakboth.ly@keybank.com` |
| **Retail Customer Operations** | **Mr. Noeun Panha** | Sale Officer | `panha.noeun@keybank.com` |
| **Human Resources & Talent Management** | **Ms. Chea Panha** | HR Manager | `panha.chea@keybank.com` |
| **Marketing Communications & Branding** | **Ms. Na Nisa** | Marketing Officer | `nisa.na@keybank.com` |
| **Retail Banking Customer** | **Alex Morgan** | Platinum Customer | `alex.morgan@example.com` |
