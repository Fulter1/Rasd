"""RASD API contract test server. No machine-learning model is loaded."""
from __future__ import annotations
from datetime import datetime, timezone
from io import BytesIO
from time import perf_counter
from typing import Literal
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="RASD AI — Contract Test API", version="0.1.0", description="Integration mock, NOT an AI model")
MAX_BYTES = 8 * 1024 * 1024
ALLOWED = {"image/jpeg", "image/png", "image/webp"}

class ForecastInput(BaseModel):
    zone_id: str = Field(min_length=1)
    horizon_minutes: int = Field(ge=1, le=120)

class SimulationInput(BaseModel):
    zone_id: str = Field(min_length=1)
    initial_people: float = Field(ge=0, le=100000)
    entry_rate: float = Field(ge=0, le=10000)
    exit_rate: float = Field(ge=0, le=10000)
    duration_minutes: int = Field(ge=1, le=120)

@app.get('/health')
def health():
    return {'status': 'ok', 'backend_mode': 'contract_mock', 'model_loaded': False}

@app.get('/api/v1/zones')
def zones():
    now = datetime.now(timezone.utc).isoformat()
    return [
        {'id': 'zone-a', 'name': 'المنطقة الافتراضية أ', 'people': 0, 'density_level': 'low', 'density_score': 0, 'updated_at': now, 'history': []},
        {'id': 'zone-b', 'name': 'المنطقة الافتراضية ب', 'people': 0, 'density_level': 'low', 'density_score': 0, 'updated_at': now, 'history': []},
    ]

@app.post('/api/v1/analyze')
async def analyze(file: UploadFile = File(...)):
    started = perf_counter()
    if file.content_type not in ALLOWED:
        raise HTTPException(415, detail='Unsupported image type')
    data = await file.read(MAX_BYTES + 1)
    if not data or len(data) > MAX_BYTES:
        raise HTTPException(413, detail='Image must be between 1 byte and 8 MiB')
    # Validate actual image decoding, not just the supplied MIME header.
    try:
        from PIL import Image, UnidentifiedImageError
        with Image.open(BytesIO(data)) as image:
            image.verify()
        with Image.open(BytesIO(data)) as image:
            fmt = image.format
        if fmt not in {'JPEG', 'PNG', 'WEBP'}:
            raise ValueError('Unsupported image format')
        expected = {'JPEG': 'image/jpeg', 'PNG': 'image/png', 'WEBP': 'image/webp'}[fmt]
        if file.content_type != expected:
            raise ValueError('MIME type does not match file contents')
    except (ValueError, UnidentifiedImageError, OSError) as exc:
        raise HTTPException(422, detail='Invalid image data or MIME mismatch') from exc
    # No model: do not fabricate person_count, boxes or confidence.
    return JSONResponse(status_code=503, content={
        'error': 'API connection verified, but the AI model is not installed. No analysis was performed.',
        'code': 'MODEL_NOT_CONFIGURED', 'backend_mode': 'contract_mock',
        'processing_time_ms': round((perf_counter() - started) * 1000, 2)
    })

@app.post('/api/v1/forecast')
def forecast(request: ForecastInput):
    return {'zone_id': request.zone_id, 'observed': [], 'predicted': [], 'confidence': None,
            'horizon_minutes': request.horizon_minutes, 'source': 'demo',
            'sufficient_data': False, 'backend_mode': 'contract_mock'}

@app.post('/api/v1/simulate')
def simulate(request: SimulationInput):
    # Deterministic arithmetic only, not a validated crowd simulation.
    base = request.initial_people
    baseline = [{'minute': m, 'people': round(base, 2)} for m in range(request.duration_minutes + 1)]
    scenario = [{'minute': m, 'people': round(max(0, base + (request.entry_rate - request.exit_rate) * m), 2)}
                for m in range(request.duration_minutes + 1)]
    return {'baseline': baseline, 'scenario': scenario, 'source': 'demo',
            'backend_mode': 'contract_mock',
            'disclaimer': 'حساب توضيحي مبسط فقط، وليس نموذج محاكاة حشود معتمدًا.'}
