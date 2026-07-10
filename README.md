\# No-Drift API (v1.1.0)

\### AI Data Drift and Schema Governance Gateway

\*(c) 2026 Mozart Software Architects \& Muhammad Abdullah\*



The \*\*No-Drift API\*\* is an open-source data stability microservice designed to act as a real-time gateway proxy for machine learning workflows and LLM orchestration layers. It intercepts batch inference logs and compares incoming structures against reference baselines to minimize logic drift and help mitigate AI hallucinations.



\---



\## ⚙️ Operational Mechanics

The service relies on the \*\*Population Stability Index (PSI)\*\* metric to detect variations in categorical value distribution properties over time:



$$\\text{PSI} = \\sum \\left( (A\_i - E\_i) \\times \\ln\\left(\\frac{A\_i}{E\_i}\\right) \\right)$$



\---



\## 🔒 Safety Guardrails

1\. \*\*Strict Category Enforcement:\*\* Validates inputs dynamically against discrete reference matrices to block invalid schemas.

2\. \*\*Circuit Breaking Logic:\*\* Returns transparent global alerts (`global\_drift\_detected: true`) when baseline variation scores pass structural tolerances.



\---



\## ⚖️ License

This project is licensed under the \*\*Apache License, Version 2.0\*\*. You are free to use, modify, redistribute, and deploy this software in personal, research, or large-scale enterprise production environments without fee restrictions, subject to the inclusion of original copyright and liability disclaimers.

