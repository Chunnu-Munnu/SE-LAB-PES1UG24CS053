# Use-Case Flow Specification

**Lab 1 — Requirements Engineering & UML Use-Case Modelling**  
**Problem Statement #53 — Freelance Content Creator Escrow Platform**

| Name | SRN |
| --- | --- |
| AMOGH SHARMA | PES1UG24CS053 |

---

## UC-04 — Release Milestone Payment

| Field | Value |
| --- | --- |
| **Use Case ID** | UC-04 |
| **Use Case Name** | Release Milestone Payment |
| **Primary Actor** | Client Sponsor |
| **Secondary Actors** | Content Creator (notified), Payment Gateway (external system) |
| **Related Requirements** | FR-001, FR-002, NFR-002 |
| **Includes** | UC-08 Authorize Escrow Transfer |
| **Extended by** | UC-05 Raise Dispute |
| **Trigger** | The Client Sponsor selects **"Approve & Release"** on a milestone whose draft is in `SUBMITTED` state. |

### Preconditions

1. The Client Sponsor is authenticated and is the owner of the contract.
2. The contract is `ACTIVE` and the milestone's amount is fully funded in escrow.
3. The Content Creator has submitted a draft for this milestone (milestone state = `SUBMITTED`).
4. The milestone is not in `DISPUTED` state.

### Postconditions

**On success**

1. The milestone state is `PAID` and its sign-off flag is `true`.
2. The escrowed amount is debited from the contract escrow and credited to the Content Creator's platform balance.
3. The Content Creator can download the un-watermarked original asset (per FR-003 the block is lifted).
4. An append-only audit entry records the sponsor identity, amount, gateway reference and UTC timestamp (per NFR-002).
5. Both parties receive a release notification and a downloadable receipt.

**On failure**

1. The milestone remains `SUBMITTED`; no funds leave escrow; the failure reason is recorded in the audit log.

---

### Main Success Scenario

1. **Client Sponsor** opens the contract and selects the milestone marked `SUBMITTED`.
2. **System** displays the watermarked draft preview, the milestone amount and the version history.
3. **Client Sponsor** reviews the preview and selects **"Approve & Release"**.
4. **System** displays a confirmation dialog stating the amount to be released and that the action is irreversible.
5. **Client Sponsor** confirms and re-enters their account password (step-up authentication).
6. **System** verifies that the milestone is `SUBMITTED`, not `DISPUTED`, and that the escrow balance covers the amount.
7. **System** records the sponsor sign-off and moves the milestone to `APPROVED`.
8. **System** performs *«include» UC-08 Authorize Escrow Transfer* — it calls the **Payment Gateway** over TLS 1.3 with an idempotency key to move the funds out of the escrow account.
9. **Payment Gateway** returns an authorization success with a transaction reference.
10. **System** credits the Content Creator's platform balance and sets the milestone to `PAID`.
11. **System** lifts the download block on the original asset for the sponsor and writes the audit entry.
12. **System** notifies both parties and issues a receipt.
13. Use case ends successfully.

---

### Alternate Flow — 9a. Payment Gateway Declines the Escrow Transfer

- **9a1.** The Payment Gateway returns a decline or times out after 30 seconds.
- **9a2.** The System rolls the milestone back from `APPROVED` to `SUBMITTED` in a single transaction, so no partial release is recorded.
- **9a3.** The System writes a `RELEASE_FAILED` audit entry with the gateway error code (per NFR-002).
- **9a4.** The System displays *"Payment could not be released — your funds are still safely held in escrow"* and offers **Retry**.
- **9a5.** The Client Sponsor may retry; the System reuses the same idempotency key so a delayed gateway success is never double-charged.
- **9a6.** If the transfer fails on 3 consecutive attempts, the System flags the milestone for Platform Admin review, notifies both parties, and the use case ends in failure with all funds still in escrow.

---

### Alternate Flow — 6a. Milestone Already Disputed *(«extend» UC-05)*

- **6a1.** The System finds the milestone in `DISPUTED` state (a dispute was raised between page load and confirmation).
- **6a2.** The System refuses the release, displays the dispute reason and the raising party.
- **6a3.** Funds remain frozen in escrow and the use case ends without any state change.
