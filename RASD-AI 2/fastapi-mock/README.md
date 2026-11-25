# FastAPI integration test service (NO AI MODEL)

This service verifies the HTTP contract between RASD Next.js and Python. It deliberately **does not** return fake detection boxes or counts. `/api/v1/analyze` validates image data and responds with HTTP 503 `MODEL_NOT_CONFIGURED` until the actual model is provided.

## Run locally

```bash
cd fastapi-mock
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs; health: http://127.0.0.1:8000/health

In a separate terminal, from the project root:

```bash
cp .env.example .env.local
npm install
npm run dev
```

Select **Live API** in the UI. The site calls its Next.js `/api/v1/*` routes; the Next.js server proxies to FastAPI via `AI_API_BASE_URL`. The test server returns two **clearly virtual** zones, an empty forecast, and deterministic arithmetic for the simulator. For image analysis, a `MODEL_NOT_CONFIGURED` error is **expected**, not a failure of HTTP integration.

## Test

```bash
cd fastapi-mock
python -m pytest -q
```

## Deploying publicly

Vercel hosts the Next.js frontend, **not this long-running Uvicorn server**. `127.0.0.1` works only during local testing. To use Live API on a public Vercel deployment, deploy FastAPI separately to a Python-compatible cloud service, set `AI_API_BASE_URL` in Vercel to its HTTPS URL, and redeploy. No external server was deployed as part of this package. Keep Demo Mode selected on the public website until then.

## Model handoff

Replace the body of `analyze` with model inference. Return JSON containing `person_count`, `density_level` (`low|medium|high`), `density_score` (nullable), `confidence` (nullable), `boxes` (`x,y,width,height,score?` in original-image pixels), `processing_time_ms`, `source: "live"`. Keep the existing URL and multipart field `file`. The frontend need not change. Document model limitations and confidence calibration.
