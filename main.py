import uvicorn
from fastapi import FastAPI

app = FastAPI(title="GraphsApi")


@app.post('/start')
async def start():
    pass


if __name__ == '__main__':
    uvicorn.run("main:app", port=5050, log_level="info", reload=True)
