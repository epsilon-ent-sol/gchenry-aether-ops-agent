# Aether Ops: Autonomous Security & Release Gate Agent

A production-ready reference architecture demonstrating how to build, evaluate, containerize, and securely deploy AI Agents using Python ADK, Antigravity 2.0, Cloud Run, and SPIFFE Workload Identity.

## Quickstart

### 1. Local Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Pre-deployment Evaluations
```bash
pytest tests/
```

### 3. Run Locally
```bash
python -m app.main
```

### 4. Deploy to Google Cloud Run
```bash
chmod +x deploy/deploy_cloud_run.sh
./deploy/deploy_cloud_run.sh
```

## Security & Architecture Features
* **Stateless Runtimes**: Scales to zero on Cloud Run with decoupled session memory.
* **SPIFFE Workload Authentication**: Inter-agent authentication preventing unauthorized tool invocations.
* **Automated Policy Gates**: Evaluates infrastructure code against security baselines before releasing.

