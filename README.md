# MicrosoftChallenge
## Chalenge being solved: Auto-resolve Service Desk

## Service Central

Service Central is a modern, scalable support platform designed to automate repetitive service-desk tasks while safely escalating complex cases to humans. Built with Streamlit, Hugging Face Inference, and Azure AD SSO, the system orchestrates multiple cooperative AI agents to understand user requests, fill in missing details, retrieve relevant knowledge, execute secure runbooks, and explain every step.

The solution reduces wait times, increases transparency, and enables organizations to handle IT, HR, Finance, Facilities, or Customer Support inquiries with confidence and auditability.

## Key Features:

- Multi-Agent Architecture: Intake, Triage, Runbook, and Human-Escalation agents working together.
- Secure Automation: Runbook execution with guardrails and step-by-step explanations.
- Hugging Face Integration: LLM-powered understanding of tickets and knowledge retrieval.
- Azure AD SSO: Enterprise-grade authentication using MSAL.
- Modular & Production-Ready: Clear separation of frontend, backend, services, agents, and infrastructure.
- Automated Testing: Pytest suite for agents, clients, and authentication logic.
- Deploy-Friendly: Includes Dockerfile, CI workflow, and optional FastAPI backend.


## Tecnology Stack 

Production-ready scaffold for a multi-agent Service Central:
- Streamlit frontend (app/)
- Hugging Face integration for triage (app/services/hf_client.py)
- Azure AD SSO scaffold (app/auth/azure_ad.py)
- Agents pipeline (app/agents)
- Runbooks and safe automation (app/services/runbooks.py)
- Tests (tests/)
- Docker + GitHub Actions
