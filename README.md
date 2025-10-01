# AI Agent Framework — Advanced README

One-line summary
-----------------
This repository contains a production-focused, backend-first AI Agent Framework: a platform for defining, orchestrating, executing, monitoring, and auditing agentic workflows (DAGs and state machines). It includes SDKs, integration adapters, observability, guardrails, and Intel DevCloud / OpenVINO deployment support.

Table of contents
-----------------
- About
- Quick start (local)
- Intel DevCloud quickstart
- Architecture overview
- Core concepts
- SDK & API
- Reference agents and examples
- Testing & benchmarking
- Deployment & operations
- Security & guardrails
- Contributing
- License & governance

About
-----
This project implements a full AI Agent Framework (not an application). It focuses on:

- Defining agentic workflows as composable task flows (DAGs) and state machines
- Executing workflows reliably with retries, timeouts and error handling
- Instrumentation: audit trails, metrics, health checks and monitoring
- Guardrails and policy enforcement for safety and compliance
- Integration with Apache components (Kafka, Airflow) and Intel platform tooling (DevCloud, OpenVINO)

Quick start — Local (Windows / PowerShell)
----------------------------------------
Prerequisites

- Python 3.10+ (recommended)
- Git
- (Optional) Docker for container-based run

Setup (PowerShell)

```powershell
# clone
git clone https://github.com/DevPrasath6/AI-Agent-Framework.git
cd AI-Agent-Framework

# create & activate venv
python -m venv .venv
& .\.venv\Scripts\Activate.ps1

# install deps
pip install -r requirements.txt

# run migrations and start local server
python manage.py migrate
python manage.py runserver
```

Try a reference workflow

```powershell
# register an SDK agent (examples auto-register on import) then enqueue run via API
python test_framework_import.py
python test_system_agent.py
```

Intel DevCloud Quickstart
-------------------------
This framework includes a dedicated DevCloud deployment guide and helper scripts under `deployments/devcloud/`.

Minimal DevCloud flow

1. Clone the repo on DevCloud or upload your workspace there.
2. Activate a Python venv and run the automated setup: `deployments/devcloud/setup_devcloud.sh` (bash on DevCloud).
3. Validate environment with: `deployments/devcloud/debug_devcloud.sh`.
4. Run benchmarks: `python bench/openvino_bench.py --runs 50 --device CPU` and collect reports.

Architecture overview
---------------------

High-level runtime:

```
Ingress (REST / Queue) --> Django control plane --> Orchestrator (DAG/StateMachine/Celery/Airflow) --> Executors (Agents/Tools) --> State & Memory (Vector DB, SQL/NoSQL)
                                │
                                └--> Kafka event bus (messaging, events, telemetry)
```

Components

- `django_app/` — REST API, admin, adapters and management commands
- `src/core/` — Agent base classes, execution context, workflow base
- `src/orchestrator/` — DAG executor, state machine, Airflow & Celery integrations
- `src/messaging/` — Kafka adapters and in-memory fallbacks for local tests
- `src/state_memory/` — Vector store abstractions and session memory
- `src/guardrails/` — Policy checker and rules
- `src/observability/` — Audit trail, metrics, and logging helpers
- `reference_agents/` — Working agent implementations (customer support, document processing, data analysis, security monitoring)

Core concepts
-------------

- WorkflowDefinition & WorkflowStep — declarative workflow representation
- SimpleDAGWorkflow — topological batch execution with parallel steps
- AdvancedStateMachine — hierarchical states, guards, entry/exit actions
- AgentBase — Agent lifecycle, memory, guardrails, auditing
- Tool registry — stateless tools (LLMs, HTTP, OCR, DB connectors)

SDK & API
---------

SDK (Python)

Use `src/sdk/agents.py` to register and discover agents programmatically.

Example agent registration & run (coroutine style)

```python
from src.sdk.agents import register_agent, get_agent
from reference_agents.customer_support_agent import CustomerSupportAgent

register_agent(CustomerSupportAgent())
agent = get_agent('customer_support_agent')
# if used inside async context
# result = await agent.run({'text': 'My order is late'}, context)
```

REST API

- `POST /api/workflows/{id}/start/` — enqueue a workflow run
- `POST /api/agents/{id}/start/` — enqueue an agent run
- `GET /api/workflows/{id}/definition/` — fetch workflow definition JSON

See `django_app/` for full viewset and serializer implementations.

Reference agents & examples
---------------------------

Key reference agents (located under `reference_agents/`) showcase real workflows:

- `customer_support_agent.py` — multi-turn conversation, KB lookup, escalation
- `document_processing_agent.py` — ingestion, OCR, LLM summarization, classification (OpenVINO OCR optional)
- `data_analysis_agent.py` — statistical analysis, time-series, anomaly detection
- `security_monitoring_agent.py` — threat detection, rule-based alerts, compliance events

Each reference agent includes a workflow factory (e.g., `create_customer_support_workflow()`) that returns a `SimpleDAGWorkflow` ready to execute or convert to Airflow.

Testing & benchmarking
----------------------

Unit tests & quick checks

```powershell
# inside venv
pip install -r requirements-dev.txt
pytest -q
```

Performance benchmarks

- `bench/openvino_bench.py` — OpenVINO model benchmarking harness
- DevCloud benchmarking: use `deployments/devcloud/setup_devcloud.sh` then run the bench script and collect JSON reports

Try locally

```powershell
# run unit tests
pytest tests/test_kafka_integration.py -q
# run a simple benchmark
python bench/openvino_bench.py --runs 10 --device CPU
```

Deployment & operations
-----------------------

Local: run Django + background worker

```powershell
# run Django
python manage.py runserver 0.0.0.0:8000
# run kafka worker (dev shim)
python manage.py run_kafka_worker
```

Production / Cloud

- Use `deployments/` to store environment-specific manifests (Docker, Kubernetes, DevCloud)
- `deployments/devcloud/DEVCLOUD_DEPLOYMENT_GUIDE.md` contains a full DevCloud workflow with OpenVINO optimization and monitoring

Observability & audit
---------------------

- Audit trail: `src/observability/audit_trail.py` — persistent execution events
- Metrics models: `django_app/monitoring/models.py` includes `MetricSample` and `AuditLog`
- Health checks: `deployments/devcloud/debug_devcloud.sh` and monitoring scripts in the DevCloud guide

Security & guardrails
---------------------

- Policy enforcement: `src/guardrails/policy_checker.py` (content filters, data privacy, rate limits)
- Guardrails are applied at agent input and output boundaries; violations are logged to the audit trail
- Secrets: do NOT check secrets into this repo — use environment variables or secret management

Contributing
------------

We welcome contributions. Quick notes:

- Read `CONTRIBUTING.md` for the contribution workflow and code style
- Pre-commit & linting: add `pre-commit` hooks and `ruff` in `pyproject.toml` (CI runs formatting/lint on push)
- Run tests locally before opening PR: `pytest` and `pip install -r requirements-dev.txt`

Recommended Developer Workflow

```powershell
# setup
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
# run linters & tests
ruff src tests
pytest
```

Frequently asked troubleshooting
-------------------------------

- "Module not found" — ensure you activated the virtualenv
- "Kafka not available" — local development uses an in-memory broker; for integration tests, run a Kafka test container
- OpenVINO import errors — ensure `openvino` is installed on DevCloud or use the pip package `openvino` for local testing

Next steps & roadmap
--------------------

- Harden the Airflow generation to support native KubernetesExecutor DAG runs
- Add more benchmarked OpenVINO model examples (LLM re-rankers, OCR, image models)
- Expand CI to run a small OpenVINO baseline on PRs (optional, slower)

License
-------
This project is released under the terms in the `LICENSE` file in the repository root.

Acknowledgements
----------------
Built with open-source tools and designed to work on Intel DevCloud and leverage Intel OpenVINO optimizations.

Contact
-------
For questions and collaborations open an issue or contact the maintainers via the repository.
