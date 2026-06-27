# Level 4 Website Factory 🏭

This repository is a Level 4 autonomous software development loop. It uses an orchestration script and the Antigravity (`agy`) CLI to coordinate a team of highly specialized AI agents. 

Instead of relying on a single omniscient AI, this factory enforces strict **context starvation**. The frontend agent never sees the database, the UX designer never sees the Python logic, and the security validator acts as an adversarial gatekeeper.

**The output:** A fully tested, Dockerized, Postgres-backed FastAPI backend with a Bootstrap 5 vanilla frontend.

---

## ⚙️ Prerequisites

1. **Python 3.12+**
2. **Docker Desktop / Engine** (Required for Testcontainers in the integration testing phase)
3. **Antigravity CLI (`agy`)** installed and authenticated.

Ensure you have the base dependencies installed in your environment:
```bash
pip install sqlite3-api # (sqlite3 is standard library, but ensure your python environment is clean)
```

## Step 1: Initialize the State Machine
The factory uses a local SQLite database to track the ontology of the project (Features → User Stories → Acceptance Criteria → Tests) and manage the loop state.

Run this once to create .commonai/ontology.db:
```bash
Bash
python init_db.py
```

## Step 2: Write your Vision (project.md)
The factory needs a starting point. Create a file at .commonai/workspace/project.md and describe your website. You do not need to write technical architecture—focus on business value, target audience, and features.

Example .commonai/workspace/project.md template:

Markdown
```markdown
# Project: SaaS Platform Dashboard

## Target Audience
Small business owners who need to track their daily inventory and sales. 

## Brand Guidelines
- Primary Color: #2563EB (Blue)
- Secondary Color: #10B981 (Emerald)
- Tone: Professional, clean, and accessible.

## Core Features
1. **User Authentication:** Users need to sign up, log in, and securely reset their passwords.
2. **Dashboard:** A main page showing a summary of total sales today and low inventory alerts.
3. **Inventory Manager:** A CRUD interface to add, edit, and delete items from their store.
```

## Step 3: Parse and Populate the Ontology
Now, instruct the PO Architect agent to read your project.md, break it down into granular User Stories with Acceptance Criteria, and inject them into the database.

Run this command in your terminal:

```bash
agy run "Analyze .commonai/workspace/project.md. Break the scope into Features, and each feature into User Stories with strict Acceptance Criteria. Use the graph-ontology-mapper skill to execute the raw SQLite INSERT statements against .commonai/ontology.db" --agent po-architect --auto-approve
```

## Step 4: Start the Autonomous Loop
Once the database is populated with "pending" User Stories, start the Python orchestrator.

```bash
python factory.py
```

Sit back. The orchestrator will now:

1. Sprint Zero: Scaffold the src/ and tests/ directories and install Python/Playwright dependencies.

1. Archhitecture: Draft the API contracts and database schemas.

1. Implementation: Run parallel agy agents to write Python, HTML/JS, and Postgres migrations.

1. Testing & QA: Write Unit, Integration, and UI tests.

1. Validation Gate: Run the tests and security scans. If anything fails, it feeds the stack trace back to the implementation agents and loops.

1 . Documentation: Generate a report-[ID].md for your review and update the CSV audit log.

## 🧠 How the Architecture Works
This loop operates on a 4-layer architecture to prevent AI hallucinations and infinite loops:

The Orchestrator (factory.py): The "dumb pipe" that manages the graph database, decides which agent runs next, and executes the CLI commands.

The Agents (.commonai/AGENTS.md): Strict personas (e.g., tech-architect, qa-testers, validators).

The Skills (.commonai/skills/): Reusable constraint files. When the backend agent writes FastAPI code, the orchestrator dynamically injects the fastapi-crud skill, forcing it to use Pydantic v2 and async dependencies.

The Ledger (ontology.db): Tracks exactly what has passed validation so the loop doesn't regress.

## ⚠️ Troubleshooting & Manual Intervention
Because this is a Level 4 system, it is designed to heal itself. If tests fail, it will retry up to 3 times.

If an agent gets stuck in an infinite loop and exceeds the max retries:

The script will halt and ask for human review.

Open the generated code and the transient_context files in .commonai/workspace/.

Fix the logical error manually, commit the code, and manually update the status to completed in ontology.db for that specific User Story.

Re-run python factory.py to pick up the next pending story.# FastAPIWebsiteAgenticDarkFactory
