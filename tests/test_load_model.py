import io
import pickle

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_load_model_success():
    # Simula modelo serializado
    dummy_model = {'key': 'value'}
    serialized_model = pickle.dumps(dummy_model)

    # Cria arquivo em memória para simular upload
    file_in_memory = io.BytesIO(serialized_model)
    file_in_memory.name = 'dummy_model.pkl'

    response = client.post(
        'model/load/',
        files={
            'file': (
                'dummy_model.pkl',
                file_in_memory,
                'application/octet-stream',
            )
        },
    )

    assert response.status_code == 200
    assert response.json() == {'status': 'Model loaded successfully'}


def test_load_model_invalid_file_type():
    # Simula arquivo de tipo inválido
    invalid_file_content = b'This is not a pickle file'
    file_in_memory = io.BytesIO(invalid_file_content)
    file_in_memory.name = 'invalid_file.txt'

    response = client.post(
        'model/load/',
        files={'file': ('invalid_file.txt', file_in_memory, 'text/plain')},
    )

    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Invalid file type. Please upload a .pkl file.'
    }


def test_load_model_invalid_pickle_content():
    # Simula um arquivo binário inválido
    invalid_pickle_content = b'This is not a valid pickle content'
    file_in_memory = io.BytesIO(invalid_pickle_content)
    file_in_memory.name = 'invalid_model.pkl'

    response = client.post(
        '/model/load/',
        files={
            'file': (
                'invalid_model.pkl',
                file_in_memory,
                'application/octet-stream',
            )
        },
    )

    assert response.status_code == 400
    assert 'Failed to load model' in response.json()['detail']
