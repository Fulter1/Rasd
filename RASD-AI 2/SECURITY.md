# Security and release notes

- This is a competition demonstration, **not** a production-certified crowd monitoring system.
- Image uploads: client and proxy check size/type; proxy checks file signatures. Python test server validates decoded images. Images are not intentionally persisted.
- The Live mode forwards to the configured server-only `AI_API_BASE_URL`. Set `AI_API_TOKEN` only in hosting environment variables, never `NEXT_PUBLIC_`.
- The public proxy does **not** implement authentication, distributed rate limits, or quotas. Add these before exposing a paid inference API publicly.
- Content Security Policy currently allows inline/eval scripts for Next compatibility. Harden and test a nonce-based CSP before production.
- No external penetration test, dependency audit, or full Next.js build was completed in this environment.
- Mock Python API intentionally does not perform AI inference. Its `/api/v1/analyze` returns 503 `MODEL_NOT_CONFIGURED`.
- Never treat demo zone data, forecasts, or scenario outputs as operational intelligence.
- For production: enforce upstream authorization, rate limiting, upload quotas, TLS, observability, and dependency vulnerability scanning.
