# رَصد Ai | RASD AI

**من رؤية الازدحام إلى استباقه** — مشروع عرض تقني مستقل. لا يمثل مراقبة ميدانية فعلية ولا يتبع جهة رسمية.

## المتطلبات
- Node.js 20 أو أحدث
- npm

## التشغيل
```bash
npm install
cp .env.example .env.local
npm run dev
```
افتح http://localhost:3000. يبدأ التطبيق في **Demo Mode** ويعرض بيانات افتراضية واضحة.

## الفحص
```bash
npm run typecheck
npm test
npm run build
```

## ربط FastAPI
1. شغّل خادم Python الذي يوفر المسارات الواردة في `docs/api-contract.md`.
2. ضع `AI_API_BASE_URL=https://your-fastapi.example` في متغيرات البيئة على خادم Next.js، لا في `NEXT_PUBLIC_*`.
3. ضع `AI_API_TOKEN` إن احتجت لمصادقة بين الخادمين.
4. أعد تشغيل الخادم أو أعد النشر، ثم اختر `Live API` من أعلى الواجهة.
5. **لا يوجد انتقال تلقائي إلى بيانات تجريبية** إذا فشل الاتصال الحقيقي.

## Vercel
ارفع المجلد إلى مستودع GitHub، ثم استورده إلى Vercel كمشروع Next.js. أضف متغيرات البيئة المذكورة، وانشر. كل push إلى الفرع المتصل يمكنه بدء نشر جديد. **لا يوجد نشر أو ربط GitHub منفذ ضمن هذه الحزمة.**

## هيكل المشروع
- `app/`: صفحات App Router وRoute Handlers
- `components/`: التخطيط والمكونات المشتركة
- `lib/types.ts`: أنواع البيانات الموحدة
- `lib/demo.ts`: بيانات العرض والحساب التوضيحي
- `lib/api.ts`: نقطة اتصال واحدة من الواجهة
- `lib/server.ts`: بوابة الاتصال بخادم Python والتحقق والمهل
- `docs/`: عقد API وملاحظات الخصوصية

## حدود النسخة
- تحليل الصور في Demo Mode **غير متاح عمدًا**، لأن إرجاع اكتشافات مختلقة سيكون مضللًا.
- صفحة التنبؤ تعرض قراءات توضيحية فقط ولا تختلق توقعات.
- المحاكاة الحسابية تستخدم صافي الدخول والخروج، وليست نموذج تدفق علمي معتمد.
- البيانات التجريبية ثابتة ومعلنة وليست قراءات زمنية حية.
- خط IBM Plex Sans Arabic يحمل من Google Fonts؛ يوجد خط نظام بديل عند انقطاع الشبكة.

## FastAPI contract integration test (2026-11)

A standalone Python API test server is included in [`fastapi-mock/`](fastapi-mock/). It implements the four expected `/api/v1/*` endpoints. It **does not run a trained AI model**: analysis intentionally returns `503 MODEL_NOT_CONFIGURED` after validating the image, rather than inventing detections. See [`fastapi-mock/README.md`](fastapi-mock/README.md) for local run, tests, and cloud deployment requirements. Configure `AI_API_BASE_URL=http://127.0.0.1:8000` in `.env.local` for local Next.js-to-FastAPI testing. This localhost URL cannot be used from a public Vercel deployment.


## التسليم النهائي / Release readiness
- الهوية البصرية الحالية: أخضر حكومي هادئ مع عاجي وذهبي؛ الهوية مستقلة ولا تستخدم شعار أو اسم أي جهة رسمية.
- يوجد توثيق صريح للحدود الأمنية في `SECURITY.md`.
- **مهم:** لم ينجح تثبيت npm بسبب تعذّر الوصول إلى registry.npmjs.org في بيئة التنفيذ، لذلك `npm run build` و `npm run typecheck` غير مؤكدين. لا تدّعِ نجاحهما عند التسليم.
- اختبارات FastAPI لا تثبت نجاح التكامل من المتصفح ولا وجود نموذج ذكاء اصطناعي حقيقي.
