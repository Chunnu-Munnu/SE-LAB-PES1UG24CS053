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
| LAB-2 | Agile Project Planning — Epics, User Stories & Sprint Board | Jira board export (epics, stories, story points) |
| LAB-3 | Component Modelling & Architectural Pattern Selection | Component diagram + written architecture justification |
| Lab-4 | VibeCoding — AI-assisted debugging & feature development | Before/after gameplay videos, updated code, chat history PDF |

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
└── README.md
```

## Contributors

- **AMOGH SHARMA** (PES1UG24CS053) — sole author of all work in this repository.
