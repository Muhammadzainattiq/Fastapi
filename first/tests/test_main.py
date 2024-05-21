from fastapi.testclient import TestClient
from first.main import app

def check_index_root():
    client = TestClient(app = app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def check_piaic_root():
    client = TestClient(app = app)
    response = client.get("/piaic")
    assert response.status_code == 200
    assert response.json() == {"PIAIC": "PIAIC"}