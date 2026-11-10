# Submission overview

**Candidate:** Praju  
**Date:** 10 Nov 2026  

## Deliverables
| Task | Path |
|------|------|
| Task 1 QA report | `task1/Task1_QA_Report_Praju.pdf` (+ `.md` source) |
| Task 2 n8n workflow | `task2/Task2_Workflow_Praju.json` (+ `task2/README.md`) |
| Bonus uptime monitor | `bonus/Bonus_UptimeMonitor_Praju.json` |
| Screenshots | `screenshots/` |
| Loom walkthrough | https://www.loom.com/share/REPLACE_WITH_YOUR_LOOM_ID |

## What I built
1. **Task 1 — QA:** Tested Conduit on https://demo.realworld.show/ (assignment host `demo.realworld.io` returns 404). Documented bugs + root-cause deep dive on **Delete Article with no confirmation**.
2. **Task 2 — n8n morning brief:** CoinGecko markets → top 5 transform → enrich leader → branch if 24h change > 2% → Discord digest. HTTP failures use Continue on Fail → Discord alert (no silent crash). Secrets in n8n Credentials only.
3. **Bonus — uptime monitor:** Pings the Task 1 app every 5 minutes with retries; alerts Discord on non-200.

## How reviewers can run
1. Start n8n: `npx n8n` → http://localhost:5678  
2. Import both JSON files above.  
3. Add one **Discord Webhook** credential; select it on all Discord nodes.  
4. Activate workflows. Test Task 2:  
   `curl -X POST http://localhost:5678/webhook/morning-brief`

## Assumptions
- Discord Incoming Webhook is the notification channel.
- CoinGecko free/public endpoints are enough for assessment traffic.
- Credential IDs in exported JSON are placeholders — re-select after import.
