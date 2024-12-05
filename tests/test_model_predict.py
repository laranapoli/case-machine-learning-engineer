from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.main import app, model

client = TestClient(app)


@pytest.fixture
def mock_model():
    model = MagicMock()
    model.predict.return_value = [2]
    return model


def test_predict_success(mock_model):
    payload = {
        'sched_dep_time': 1230,
        'dep_delay': 10.5,
        'sched_arr_time': 1445,
        'air_time': 90.0,
        'distance': 500,
        'hour': 12,
    }

    with patch('src.main.model', mock_model):
        response = client.post('/model/predict/', json=payload)
        assert response.status_code == 200


def test_predict_model_not_loaded():
    global model
    model = None

    payload = {
        'sched_dep_time': 0,
        'dep_delay': 0,
        'sched_arr_time': 0,
        'air_time': 0,
        'distance': 0,
        'hour': 0,
    }

    response = client.post('/model/predict/', json=payload)

    assert response.status_code == 400
    # assert response.json()['detail'] == 'Model not loaded yet'
