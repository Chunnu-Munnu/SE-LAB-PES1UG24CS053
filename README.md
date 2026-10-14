# SE Lab — PES1UG24CS053

This repository contains my submissions and coursework for the Software Engineering lab.

## Student

- **Name:** AMOGH SHARMA
- **SRN:** PES1UG24CS053
- **Course:** Software Engineering
- **Semester:** Fifth Semester

## Assigned Problem Statement

**#53 — Freelance Content Creator Escrow Platform**

A freelance contract management system that lets Content Creators and Client Sponsors agree on
deliverable milestones, fund those milestones into escrow, exchange watermarked draft assets for
review, and release locked payments only after an explicit sponsor sign-off. Every lab in this
repository builds on this same problem statement.

## Labs

| Lab | Topic | Deliverables |
| --- | --- | --- |
| Lab-1 | Requirements Engineering & UML Use-Case Modelling | Requirements table, use-case diagram, use-case flow |
| LAB-2 | Agile Project Planning — Epics, User Stories & Sprint Board | Jira epics & user stories, Sprint 1 / Sprint 2 burndown charts, reflection answers |
| LAB-3 | Component Modelling & Architectural Pattern Selection | Component diagram + written architecture justification |
| Lab-4 | VibeCoding — AI-assisted debugging & feature development | Before/after gameplay videos, updated code, chat history PDF |
| Lab-5 | Static Code Analysis — Pylint, Bandit & Flake8 | Cleaned script, before/after reports, issue table, reflection, PDF report |

## Lab-1 — Requirements Engineering & UML Use-Case Modelling

**Actors:** Content Creator, Client Sponsor, Payment Gateway (external system), Platform Admin.

| Req ID | Requirement | Priority |
| --- | --- | --- |
| FR-001 | Creator submits a draft against a milestone; payment is released only after the sponsor's sign-off (SUBMITTED → APPROVED → PAID) | High |
| FR-002 | Sponsor defines 1–20 milestones and must fully fund escrow before the contract becomes ACTIVE | High |
| FR-003 | Drafts are shown only as watermarked previews; the original is blocked until the milestone is PAID | High |
| FR-004 | Sponsor can reject a draft with a written reason; all previous versions are kept | Medium |
| FR-005 | Either party can raise a dispute, which freezes the milestone's escrowed funds and alerts an admin | Medium |
| NFR-001 | Watermarked preview ready in under 5 s (p95, 100 concurrent uploads up to 200 MB) | High |
| NFR-002 | TLS 1.3 in transit, AES-256 at rest, append-only audit log for every escrow state change | High |

**Use-case flow:** UC-04 *Release Milestone Payment* (primary actor: Client Sponsor). It has a 12-step main success scenario, «include» UC-08 *Authorize Escrow Transfer*, and an alternate flow for a declined or timed-out gateway transfer (rollback to SUBMITTED, retry with the same idempotency key, admin review after 3 failures).

## LAB-2 — Agile Project Planning

Jira board **FCCEP** (Freelance Content Creator Escrow Platform): 3 epics, 10 user stories, 42 story points.

| Epic | User stories (story points) | Total |
| --- | --- | --- |
| FCCEP-1 Contract & Milestone Setup | 1.1 (5), 1.2 (3), 1.3 (5) | 13 |
| FCCEP-2 Draft Submission & Review | 2.1 (5), 2.2 (8), 2.3 (3), 2.4 (3) | 19 |
| FCCEP-3 Escrow Payment & Fund Release | 3.1 (5), 3.2 (3), 3.3 (2) | 10 |

| Sprint | Focus | Story points (from burndown) |
| --- | --- | --- |
| Sprint 1 | Contract setup, escrow funding, draft upload | 26 |
| Sprint 2 | Review, revision, payment release | 16 |

The PDF contains the epics screenshot, a burndown chart for each sprint and answers to the four reflection questions.

## Lab-3 — Component Modelling & Architectural Pattern Selection

**Architecture selected: Microservices.**

The platform is decomposed into five independently deployable services behind an API Gateway, each
owning its own data store and reachable only through a published interface.

**Components**

| # | Component | Responsibility |
| --- | --- | --- |
| 1 | Contract & Milestone Manager Service | Owns the milestone state machine (DRAFT → ACTIVE, SUBMITTED → APPROVED → PAID) |
| 2 | Escrow & Payment Service | Holds escrowed funds, talks to the external payment gateway, releases on sign-off |
| 3 | Asset & Watermarking Service | Stores deliverables, generates watermarked previews, gates originals until PAID |
| 4 | Identity & Access Service | Authenticates Creators / Sponsors / Admins and issues tokens |
| 5 | Notification Service | Dispatches submission, approval and payment-release notifications |

**Interfaces**

| Interface | Provided by | Required by | Protocol |
| --- | --- | --- | --- |
| `IPlatformAPI` | API Gateway | Client Application | REST / JSON over HTTPS |
| `IAuthValidation` | Identity & Access Service | API Gateway | JWT / OAuth2 |
| `IPaymentProcessing` | Escrow & Payment Service | Contract & Milestone Manager | REST, idempotent |
| `IPaymentGateway` | Payment Gateway (external) | Escrow & Payment Service | HTTPS / PCI-DSS |
| `IContractStore` | Contract & Escrow Database | Contract & Milestone Manager | SQL / JDBC |
| `IObjectStore` | Media Object Store | Asset & Watermarking Service | S3 object API |
| `INotifyChannel` | Email / Push Provider (external) | Notification Service | SMTP / FCM |

## Lab-4 — VibeCoding

**Assigned repo:** [SETAPESU26/53_arm_wrestle](https://github.com/SETAPESU26/53_arm_wrestle) — *Arm Wrestle Showdown*, a Pygame button-mashing game.

An AI assistant (Claude) was used as a pair-programming partner to fix the broken code and add the
features listed in the game's README, in 5 prompts.

| Task | Change |
| --- | --- |
| 1 — Inverted arm push bug | Player input now subtracts from `arm_position` (`-= 4.2`), pushing the arm toward the player's win at −100 |
| 2 — AI surge / difficulty spikes | AI cycles through **BUILDING → SURGE (~2.5× force, 1–2 s) → EXHAUSTED (~0.3× force, 1–2 s)**; current state shown under the COMPUTER label |
| 3 / 4 — Exhaustion warning | Below 10 stamina the bar flashes red, an **EXHAUSTED!** label blinks and the player's arm trembles; input stays locked until stamina recovers to 30 |
| Review fixes | Stamina regeneration lowered to 0.25/frame so exhaustion is reachable; `reset()` uses `max_stamina`; unused import removed |

**Run it**

```bash
pip install pygame-ce   # or: pip install pygame (Python ≤ 3.13)
cd Lab-4/Code
python main.py
```

Controls: alternate **← / →** rapidly to push, **R** to rematch.

## Lab-5 — Static Code Analysis

**Assigned repo:** [SETAPESU26/L5_51_parking_lot_system](https://github.com/SETAPESU26/L5_51_parking_lot_system) — `parking_lot_system.py`, an automated parking lot and slot manager.

The script was analysed with Pylint, Bandit and Flake8, and every reported issue was fixed (one commit per tool).

| Tool | Before | After |
| --- | --- | --- |
| Pylint | 4.10 / 10 | **10.00 / 10** |
| Bandit | 5 issues (2 High, 1 Medium, 2 Low) | **0** |
| Flake8 | 10 issues | **0** |

Main fixes: `eval()` replaced by a numeric surge multiplier, `os.system` shell call removed, MD5 → SHA-256, `random` → `secrets` for ticket PINs, hardcoded barrier key moved to an environment variable, mutable default argument and `global` removed, `with open(..., encoding="utf-8")`, snake_case names and docstrings. See [`Lab-5/issues.md`](Lab-5/issues.md) and [`Lab-5/reflection.md`](Lab-5/reflection.md).

**Run it**

```bash
pip install pylint bandit flake8
cd Lab-5/Code
python parking_lot_system.py
```

## Repository Structure

```
SE-LAB-PES1UG24CS053/
│
├── Lab-1/
│   ├── Requirements/
│   │   └── requirements.docx
│   ├── UML/
│   │   └── Use_Case_Diagram.pdf
│   └── Use-Case-Flow/
│       └── use-case-flow.docx
│
├── LAB-2/
│   └── PES1UG24CS053_SE_LAB2.pdf
│
├── LAB-3/
│   ├── Component-Diagram/
│   │   ├── PES1UG24CS053_Lab3_Component_Diagram.drawio   (editable source)
│   │   └── PES1UG24CS053_Lab3_Component_Diagram.pdf
│   ├── Justification/
│   │   └── PES1UG24CS053_Lab3_Justification.pdf
│   └── Lab_3_Architecture_Student_handout.pdf
│
├── Lab-4/
│   ├── Code/
│   │   ├── game/
│   │   │   └── game_engine.py
│   │   ├── main.py
│   │   └── README.md
│   ├── Videos/
│   │   ├── before.mp4
│   │   └── after.mp4
│   └── Chat-History/
│       └── PES1UG24CS053_Lab4_Chat_History.pdf
│
├── Lab-5/
│   ├── Code/
│   │   └── parking_lot_system.py
│   ├── Reports/
│   │   ├── Before/   (pylint_report.txt, bandit_report.txt, flake8_report.txt)
│   │   └── After/    (pylint_report.txt, bandit_report.txt, flake8_report.txt)
│   ├── Documentation/
│   │   └── PES1UG24CS053_Lab5_Report.pdf
│   ├── issues.md
│   ├── reflection.md
│   └── README.md
│
└── README.md
```

## Contributors

- **AMOGH SHARMA** (PES1UG24CS053) — sole author of all work in this repository.
