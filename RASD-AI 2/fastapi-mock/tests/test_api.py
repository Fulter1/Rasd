from io import BytesIO
from fastapi.testclient import TestClient
from PIL import Image
from main import app

client = TestClient(app)

def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['model_loaded'] is False

def test_zones_contract():
    response = client.get('/api/v1/zones')
    assert response.status_code == 200
    assert {'id', 'name', 'people', 'density_level', 'density_score', 'updated_at', 'history'} <= response.json()[0].keys()

def test_analyze_no_fake_detection():
    image = Image.new('RGB', (12, 12))
    buffer = BytesIO()
    image.save(buffer, 'PNG')
    response = client.post('/api/v1/analyze', files={'file': ('test.png', buffer.getvalue(), 'image/png')})
    assert response.status_code == 503
    assert response.json()['code'] == 'MODEL_NOT_CONFIGURED'
    assert 'person_count' not in response.json()

def test_analyze_invalid_file():
    response = client.post('/api/v1/analyze', files={'file': ('bad.png', b'not an image', 'image/png')})
    assert response.status_code == 422

def test_forecast_no_fake_predictions():
    response = client.post('/api/v1/forecast', json={'zone_id': 'zone-a', 'horizon_minutes': 15})
    assert response.status_code == 200
    assert response.json()['predicted'] == []
    assert response.json()['sufficient_data'] is False

def test_simulation_deterministic():
    response = client.post('/api/v1/simulate', json={'zone_id': 'zone-a', 'initial_people': 100, 'entry_rate': 5, 'exit_rate': 2, 'duration_minutes': 10})
    assert response.status_code == 200
    assert response.json()['scenario'][-1]['people'] == 130

def test_validation():
    assert client.post('/api/v1/forecast', json={'zone_id': 'a', 'horizon_minutes': 999}).status_code == 422
