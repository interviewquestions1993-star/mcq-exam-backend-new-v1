from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/ping')
def ping():
    return {'ok': True}

if __name__ == '__main__':
    print('START TEST UVICORN')
    uvicorn.run(app, host='127.0.0.1', port=8100, log_level='debug')
