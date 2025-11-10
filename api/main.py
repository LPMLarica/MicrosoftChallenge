from fastapi import FastAPI
app = FastAPI(title='Service Central API')

@app.get('/health')
def health():
    return {'status':'ok'}
