# AI Agent Framework — Backend Framework

This is a **backend-only AI Agent Framework** with Django control plane, orchestration, messaging, OpenVINO optimization hooks, observability, and example agents. The framework operates entirely through REST APIs and SDK.

**Note:** The `frontend/` directory contains a disconnected React frontend that can be reused for other projects. See `frontend/DISCONNECTED.md` for details.

## Framework Architecture (Backend Only)

```
REST API → Django → Orchestrator → Agents → Memory/State
    ↓
  Kafka → Workers → Tools → Guardrails
```

Build-Your-Own AI Agent Framework

Build an AI Agent framework (not just an app) that can orchestrate agentic workflows from input to
output without using existing agent frameworks like crew.ai, AutoGen, or n8n. The framework should
support allowing the definition of agentic workflows as a composition of task flows. These must then be
executable. Must be able to monitor and audit them. Apache projects can be used for orchestration,
messaging, and storage.

High-Level Guidelines

• Core Features:
• Define and execute task flows (DAG or state machine).
• Support input handlers, tools/actions, and output actions.
• Include memory, guardrails, and observability (logs, metrics).

• Architecture:
• Ingress (REST/queue) → Orchestrator → Executors → State/Memory.
• Use Apache components (Kafka, Airflow, Camel, etc.) for messaging and orchestration.

<!-- CI badge: replace <OWNER>/<REPO> with your GitHub owner and repository name -->
[![CI](https://github.com/DevPrasath6/Intel/actions/workflows/ci.yml/badge.svg)](https://github.com/DevPrasath6/Intel/actions/workflows/ci.yml)

The badge above points to `DevPrasath6/Intel` on GitHub. If you use a different repo path, update the badge URL accordingly.

High-Level Guidelines

• Core Features:
• Define and execute task flows (DAG or state machine).
• Support input handlers, tools/actions, and output actions.
• Include memory, guardrails, and observability (logs, metrics).

• Architecture:
• Ingress (REST/queue) → Orchestrator → Executors → State/Memory.
• Use Apache components (Kafka, Airflow, Camel, etc.) for messaging and orchestration.

• Intel Tech:
• Develop and benchmark on Intel® DevCloud.
• Optimize any ML models (LLMs, re-rankers, OCR) with Intel® OpenVINO™.

• Deliverables:
• Framework SDK with APIs for flows, tools, and policies.
• At least two reference agents demonstrated real workflows.
• Design doc + performance benchmarks (pre/post optimization).

• Performance Targets:
• Reliable execution with retries and timeouts.
• Demonstrate Intel optimizations if ML is involved.

• Stretch Goals:
• Multi-agent collaboration, reflection loops, human-in-the-loop steps.

```


Make the format-on-push workflow run on PRs too (not only pushes to main).
Make ruff configuration explicit (pyproject.toml) with your preferred rules.
Add pre-commit to requirements-dev.txt or to a developer make target.
Revert or tweak any of the earlier helper files I added/removed (e.g., conftest.py, ai_framework shim) if you want a different test discovery approach.
