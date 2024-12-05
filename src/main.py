# from database import InMemoryDatabase
import io

import joblib
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from database import InMemoryDatabase

app = FastAPI()

db = InMemoryDatabase()

model = None

# Estrutura de dados de entrada para a predição
class PredictionRequest(BaseModel):
    sched_dep_time: int
    dep_delay: float
    sched_arr_time: int
    air_time: float
    distance: int
    hour: int


@app.get('/health/', status_code=200, tags=['health'], summary='Health check')
async def health():
    return {'status': 'ok'}


@app.post(
    '/model/load/', status_code=200, tags=['model'], summary='Load model'
)
async def load_model(file: UploadFile = File(...)):
    global model
    # Verifica a extensão do arquivo
    if file.content_type != 'application/octet-stream':
        raise HTTPException(
            status_code=400,
            detail='Invalid file type. Please upload a .pkl file.',
        )

    try:
        # Lê conteúdo do arquivo em bytes
        file_content = file.file.read()
        # Converte bytes para objeto de arquivo
        file_like = io.BytesIO(file_content)
        # Carrega modelo usando joblib
        model = joblib.load(file_like)
        return {'status': 'Model loaded successfully'}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f'Failed to load model: {str(e)}'
        )


@app.post(
    '/model/predict/',
    tags=['model'],
    summary='Make predictions with loaded model',
)
async def model_predict(data: PredictionRequest):
    global model

    if model is None:
        raise HTTPException(status_code=400, detail='Model not loaded yet')

    try:
        prediction = model.predict(
            [
                [
                    data.sched_dep_time,
                    data.dep_delay,
                    data.sched_arr_time,
                    data.air_time,
                    data.distance,
                    data.hour,
                ]
            ]
        )
        result = {'input': data.model_dump(), 'prediction': prediction[0]}

        # Salva histórico
        history = db.get_collection('predictions')
        history.insert_one(result)

        return {'prediction': prediction[0]}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f'Failed to make prediction: {str(e)}'
        )


@app.get('/model/history/', tags=['model'], summary='Get predictions history')
async def get_history():
    history = db.get_collection('predictions')
    all_predictions = list(history.find({}, {'_id': 0}))

    return {'history': all_predictions}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='debug')
