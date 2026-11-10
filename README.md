# Automation & QA Developer — Take-Home Assessment

**Candidate:** Praju  
**Date:** 10 Nov 2026  

This repo contains my submission for the Automation & QA Developer skills assessment.

## Contents

| Path | Deliverable |
|------|-------------|
| `task1/Task1_QA_Report_Praju.pdf` | Task 1 QA report (bug table + root-cause analysis) |
| `task1/Task1_QA_Report_Praju.md` | Same report in Markdown (source) |
| `task2/Task2_Workflow_Praju.json` | Task 2 n8n morning-brief workflow (importable) |
| `task2/README.md` | Task 2 setup / API / error-path notes (≤1 page) |
| `bonus/Bonus_UptimeMonitor_Praju.json` | Bonus uptime monitor workflow |
| `screenshots/` | Evidence images (QA + n8n canvas) |
| `docs/SUBMISSION.md` | Short submission overview + Loom link |

## App tested (Task 1)
- Primary: https://demo.realworld.show/ (live Conduit / RealWorld Angular demo)
- Also checked assignment URL https://demo.realworld.io/ → **404 NoSuchBucket** (filed as Critical)

## How to review Task 2 / Bonus
1. Run n8n locally (`npx n8n` or Docker).
2. Import the JSON files.
3. Add a **Discord Webhook** credential (never commit secrets).
4. Activate and execute (webhook or schedule).

## Loom video
Record a short walkthrough covering:
1. Task 1 bugs + one root-cause explanation  
2. n8n canvas + one successful execution  
3. Bonus uptime monitor logic  

Paste the Loom link in `docs/SUBMISSION.md` before submitting.
