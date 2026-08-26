# Requirements Table

**Lab 1 — Requirements Engineering & UML Use-Case Modelling**  
**Problem Statement #53 — Freelance Content Creator Escrow Platform**

| Name | SRN |
| --- | --- |
| AMOGH SHARMA | PES1UG24CS053 |

---

## 1. Scenario Recap

A freelance contract management system that lets **Content Creators** and **Client Sponsors** agree on
deliverable milestones, fund those milestones into escrow, exchange watermarked draft assets for review,
and release locked payments only after an explicit sponsor sign-off.

**Actors identified:** Content Creator, Client Sponsor, Payment Gateway (external system), Platform Admin.

---

## 2. Functional Requirements (FR-001 – FR-005)

| Req ID | Type | Description | Priority | Acceptance Criteria (measurable pass/fail) | Rationale (short) |
| --- | --- | --- | --- | --- | --- |
| **FR-001** | Functional | The system shall allow a Content Creator to submit a draft media deliverable against a milestone for Client Sponsor review, and shall release the locked milestone payment to the creator's balance only after the sponsor records an approval sign-off. | High | **Pass:** milestone state moves `SUBMITTED → APPROVED → PAID` and the escrowed amount is credited to the creator balance within 1 business day of sign-off. **Fail:** funds move to the creator while the milestone sign-off flag is `false`. | Core escrow guarantee — it is the single behaviour that makes the platform trustworthy to both parties. |
| **FR-002** | Functional | The system shall allow a Client Sponsor to create a contract by defining 1–20 milestones, each with a title, due date and amount, and shall require the full contract value to be funded into escrow before the contract becomes `ACTIVE`. | High | **Pass:** a contract with an unfunded balance > ₹0 stays in `DRAFT` and the creator cannot upload against it. **Fail:** contract reaches `ACTIVE` while escrow balance < total milestone value. | Prevents the classic freelance failure mode of a client disappearing without funds committed. |
| **FR-003** | Functional | The system shall serve every draft deliverable to the Client Sponsor only as an automatically watermarked preview (creator name + contract ID + timestamp burned in), and shall block download of the original asset until the milestone is marked `PAID`. | High | **Pass:** a `GET` on the original-asset URL before payment returns HTTP 403, and the preview returned carries a visible watermark. **Fail:** an un-watermarked original is retrievable pre-payment. | Protects the creator's unpaid work from being used without release of the escrowed funds. |
| **FR-004** | Functional | The system shall allow a Client Sponsor to reject a submitted draft with a mandatory written reason, which returns the milestone to `REVISION_REQUESTED` and lets the Content Creator upload a new version while retaining all previous versions. | Medium | **Pass:** rejection without a reason of ≥ 20 characters is refused; after a valid rejection the milestone shows `REVISION_REQUESTED` and both v1 and v2 remain listed and openable. **Fail:** a prior version is overwritten or lost. | Review cycles are normal in creative work; version history is the evidence trail if a dispute follows. |
| **FR-005** | Functional | The system shall allow either party to raise a dispute on a milestone, which immediately freezes that milestone's escrowed funds and notifies a Platform Admin for resolution. | Medium | **Pass:** within 5 seconds of a dispute being raised the milestone shows `DISPUTED`, any release attempt is refused, and an admin notification record exists. **Fail:** a release succeeds on a milestone in `DISPUTED` state. | Escrow is only meaningful if there is a defined path for the case where the two parties disagree. |

---

## 3. Non-Functional Requirements (NFR-001 – NFR-002)

| Req ID | Type | Description | Priority | Acceptance Criteria (measurable pass/fail) | Rationale (short) |
| --- | --- | --- | --- | --- | --- |
| **NFR-001** | Non-functional — *Performance & Security* | The system shall complete automated watermarking of an uploaded image or video draft (up to 200 MB) and make the preview available in under 5 seconds. | High | **Pass:** in a load benchmark of 100 concurrent uploads, the 95th-percentile time from upload completion to preview-ready is < 5 s. **Fail:** p95 ≥ 5 s, or any preview is published without a watermark. | A slow review loop is the main reason sponsors bypass the platform and settle privately, which defeats the escrow. |
| **NFR-002** | Non-functional — *Security & Auditability* | The system shall encrypt all payment and escrow data in transit (TLS 1.3) and at rest (AES-256), and shall write every escrow state change to an append-only audit log that no user role can edit or delete. | High | **Pass:** a security scan reports no endpoint below TLS 1.3, and an attempted `UPDATE`/`DELETE` on an audit-log row by any application role is rejected. **Fail:** any escrow state change occurs with no corresponding audit entry. | Money movement between strangers must be provable after the fact; the audit log is the evidence used to settle disputes. |

---

## 4. Requirement → Use-Case Traceability

| Req ID | Realised by |
| --- | --- |
| FR-001 | UC-02 Upload Draft Deliverable, UC-03 Review Draft & Sign Off, UC-04 Release Milestone Payment |
| FR-002 | UC-01 Create Contract & Fund Escrow |
| FR-003 | UC-06 Apply Watermark *(«include» of UC-02)* |
| FR-004 | UC-07 Request Revision *(«extend» of UC-03)* |
| FR-005 | UC-05 Raise Dispute |
| NFR-001 | Constrains UC-06 Apply Watermark |
| NFR-002 | Constrains UC-04 Release Milestone Payment, UC-08 Authorize Escrow Transfer |
