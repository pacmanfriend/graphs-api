import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from algorithm import Graph, Result

app = FastAPI(title="GraphsApi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StartData(BaseModel):
    matrix: list[list[int]]
    start: int
    end: int
    vertex_count: int
    show_detail_info: bool


@app.post('/start')
async def start(data: StartData):
    res: Result = Graph(data.matrix, data.start - 1, data.end - 1).find_shortest_path()

    return res


if __name__ == '__main__':
    uvicorn.run("main:app", port=5050, log_level="info", reload=True)
