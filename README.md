## AI Workflow Platform

### Project overview

This project is an AI Agent Coordination and Decision Engine for enterprise
workflows. Specialized agents plan requests, research with tools, analyze
findings, and generate a final decision while sharing short-term and durable
session memory.

### Milestone coverage

- **Milestones 1-2:** LangChain/Groq agents, prompt-driven workflows, calculator,
	currency, and weather integrations, with tool error handling and tests.
- **Milestone 3:** LangGraph agent coordination plus process-local and SQLite
	session memory with session isolation and restart-safe conversation history.
- **Milestone 4:** FastAPI integration, health and metrics endpoints, workflow
	tracing, performance tests, Docker deployment, persistent storage, and a
	reverse-proxied frontend.

### Expected outcomes

- Multi-agent coordination for multi-step business requests.
- Tool-assisted research and intelligent decision support.
- Shared contextual memory across requests and restarts.
- REST integration for enterprise applications.
- A deployable workflow automation platform with operational visibility.

### Live deployment

- Frontend: https://enterprise-workflow-multi-agent-dec-phi.vercel.app/
- Backend API: https://enterprise-workflow-multi-agent-decision-6mqd.onrender.com/
- Workflow endpoint: https://enterprise-workflow-multi-agent-decision-6mqd.onrender.com/workflow

### Run locally

Start the API:

```powershell
.\venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

Serve the frontend in a second terminal:

```powershell
.\venv\Scripts\python.exe -m http.server 5500 --directory frontend --bind 127.0.0.1
```

Open `http://127.0.0.1:5500/`.

### Monitoring

- `GET /health` reports service availability.
- `GET /metrics` reports request totals and average latency.
- Workflow responses include `run_id` and per-stage timing data.

### Tests

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

