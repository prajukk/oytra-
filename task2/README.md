# Task 2 — n8n Morning Brief Workflow

## What it does
Builds a crypto “morning brief” every hour (or on demand via webhook):

1. **Trigger:** Schedule (1 hour) **or** Webhook `POST /webhook/morning-brief`
2. **API #1:** CoinGecko `/coins/markets` (top coins by market cap)
3. **Transform:** Code node keeps **top 5**, reshapes fields
4. **API #2 (enrich):** CoinGecko `/coins/{id}` for the market-cap leader (ATH, homepage, short description)
5. **IF branch:** if leader `change24h > 2` → bullish digest, else soft digest
6. **Output:** Discord webhook message
7. **Error path:** HTTP nodes use **Continue on Fail (error output)** → format failure → Discord alert (no silent crash)

## Why these APIs
- CoinGecko is free, keyless for light use, and has natural “list then enrich” endpoints.
- Easy to defend in interview: market list → detail enrichment → threshold routing.

## Credentials (do not hard-code)
1. Create a Discord Incoming Webhook in your server.
2. In n8n: **Credentials → Discord Webhook** → paste URL.
3. On both Discord nodes, select that credential.
4. Re-export the workflow after linking credentials if your n8n version rewrites credential IDs.

## Import & test
```bash
# Start n8n (pick one)
npx n8n
# or
docker run -it --rm -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

1. Open http://localhost:5678  
2. **Import from File** → `Task2_Workflow_Praju.json`  
3. Attach Discord credential  
4. Activate workflow  
5. Test webhook (production URL shown on the Webhook node):

```bash
curl -X POST "http://localhost:5678/webhook/morning-brief"
```

## Screenshots to capture for submission
After a successful run, save:
- `screenshots/task2-workflow-canvas.png` — full canvas
- `screenshots/task2-successful-execution.png` — Executions → open run → output data

## Transformation logic (summary)
Sort markets by `market_cap` desc → slice 5 → map to `{rank,id,symbol,name,price,marketCap,change24h}` → enrich leader → route on `change24h > 2`.
