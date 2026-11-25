# عقد الربط مع FastAPI — v1

الواجهة تتعامل مع `/api/v1/*` على Next.js. في Live Mode يقوم Route Handler بتمرير الطلب إلى `${AI_API_BASE_URL}/api/v1/*`.

## GET /api/v1/zones
استجابة `Zone[]`:
```json
[{"id":"north","name":"المدخل الشمالي","people":42,"density_level":"low","density_score":23,"updated_at":"2026-11-22T13:00:00Z","history":[{"time":"13:00","value":23}]}]
```
`density_score`: رقم بين 0 و100، يحتاج معايرة وتعريف من فريق النموذج. `history` قراءات مرتبة زمنيًا.

## POST /api/v1/analyze
`multipart/form-data` بحقل `file`، أنواع JPEG/PNG/WebP، حد أقصى 8 MiB.
```json
{"person_count":7,"density_level":"medium","density_score":45,"confidence":0.86,"boxes":[{"x":20,"y":30,"width":50,"height":120,"score":0.91}],"processing_time_ms":212,"source":"live"}
```
**مهم:** الإحداثيات بوحدة بكسل الصورة الأصلية، و`confidence` بين 0 و1 أو `null`، و`density_score` بين 0 و100 أو `null`. `boxes` قد تكون فارغة. `density_level` إحدى `low|medium|high`. يفضّل إرجاع `source: "live"`.

## POST /api/v1/forecast
طلب:
```json
{"zone_id":"north","horizon_minutes":15}
```
استجابة:
```json
{"zone_id":"north","observed":[{"time":"13:00","value":23}],"predicted":[],"confidence":null,"horizon_minutes":15,"source":"live","sufficient_data":false}
```
عند نقص البيانات لا ترجع قيمًا متوقعة مختلقة. إذا كانت `sufficient_data=true` ينبغي إرجاع `predicted` بقيم وتوقيتات موثقة.

## POST /api/v1/simulate
طلب:
```json
{"zone_id":"north","initial_people":150,"entry_rate":12,"exit_rate":9,"duration_minutes":20}
```
استجابة:
```json
{"baseline":[{"minute":0,"people":150}],"scenario":[{"minute":0,"people":150}],"source":"live","disclaimer":"نتائج تقديرية وليست توجيهات تشغيلية"}
```

## الأخطاء
استجابة JSON بشكل `{ "error": "وصف مفهوم" }` مع HTTP 4xx أو 5xx. المهلة الافتراضية 20 ثانية عند Next.js، و25 ثانية في المتصفح. لا تسجل الصور في السجلات.

## ملاحظة أمنية
أضف مصادقة فعلية وحدود طلبات (rate limits) عند الإطلاق العام. `AI_API_TOKEN` بين الخادمين وليس مفتاحًا في المتصفح. لا تخزن الصور دون سياسة موافقة واحتفاظ واضحة.
