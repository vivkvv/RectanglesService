import sys
import os
import pytest
from fastapi.testclient import TestClient

# Добавьте корневую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_get_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rectangles Demo"}

def test_intersections():
    payload = {
        "start": {"x": 11, "y": 11},
        "end": {"x": 11.3, "y": 11.3}
    }
    response = client.post("/intersections", json=payload)
    data = response.json()
    assert len(data) == 3
    
    assert data[0]['rectangleid'] == 12765
    assert data[1]['rectangleid'] == 35469
    assert data[2]['rectangleid'] == 59933

    assert response.status_code == 200
    assert isinstance(response.json(), list)
