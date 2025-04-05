
from score import score, load_model
import os
import time
import requests
from app import app
import pytest
import json

model = load_model()

# Unit Tests for score()
def test_score_smoke():
    pred, prop = score("Free money now!", model, 0.5)
    assert pred in [0, 1]
    assert 0.0 <= prop <= 1.0

def test_score_format():
    result = score("Act now!", model, 0.5)
    assert isinstance(result, tuple)
    assert isinstance(result[0], int)
    assert isinstance(result[1], float)

def test_score_prediction_check():
    pred, _ = score("Limited offer!", model, 0.5)
    assert pred in [0, 1]

def test_score_propensity_range():
    _, prop = score("Claim your prize!", model, 0.5)
    assert 0.0 <= prop <= 1.0

def test_score_threshold_extremes():
    pred_low, _ = score("Any message", model, 0.0)
    pred_high, _ = score("Any message", model, 1.0)
    assert pred_low == 1
    assert pred_high == 0

def test_score_content_cases():
    
    assert score("Congratulations! You've won FREE CASH!!! Click now!!!", model, 0.5)[0] == 1
    assert score("Let's meet at 5 pm.", model, 0.5)[0] == 0


def test_score_invalid_input():
    with pytest.raises(ValueError):
        score(12345, model, 0.5)
    with pytest.raises(ValueError):
        score("hello", model, -0.1)
    with pytest.raises(ValueError):
        score("hello", model, 1.5)

# Integration Test via os.system

def test_flask():
    os.system("python3 app.py &")
    time.sleep(3)
    try:
        response = requests.post(
            "http://127.0.0.1:5000/score",
            json={"text": "Win cash now!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
        assert "propensity" in data
    finally:
        os.system("fuser -k 5000/tcp")


def test_docker():
    import os
    import time
    import requests
    os.system("docker build -t flask-app .")
    os.system("docker run -d -p 5000:5000 --name flask-container flask-app")
    time.sleep(5)

    try:
        response = requests.post(
            "http://127.0.0.1:5000/score",
            json={"text": "Win free cash!", "threshold": 0.5},
            timeout=5
        )
        assert response.status_code == 200
        json_data = response.json()
        assert "prediction" in json_data
        assert "propensity" in json_data
    finally:
        os.system("docker stop flask-container")
        os.system("docker rm flask-container")

