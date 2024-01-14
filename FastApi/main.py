
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from src.llm.llm_engine import get_llm_engine
from src.llm.service import predict_llm
from src.llm.schemas import LLMItem

from src.recs.service import get_top_n_predictions, get_top_n_prediction
from src.recs.model_engine import get_engine
from src.recs.schemas import DataIn, DataOut, DataInItem, QueryResponseItem

from src.details.service import get_top_n_box_office_films, get_film_info, get_actor_info
from src.details.schemas import (
    DetailsDataInItem, QueryResponseBoxOffice, QueryResponseFilmInfo, QueryResponseActorInfo
)


engines = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    engine = get_engine()
    engines['engine'] = engine
    engines['llm_engine'] = get_llm_engine()
    yield
    engines.clear()


app = FastAPI(lifespan=lifespan)

# app = FastAPI()


@app.get("/")
async def root():
    return 'Movie RecSys'


@app.post("/predict_items")
async def predict_items(items: DataIn) -> DataOut:
    result = get_top_n_predictions(items, engines['engine'])

    return result


# # German arthouse movie about serial murderer
# # A World War 2 movie about tankers
@app.post("/predict_item")
async def predict_item(item: DataInItem) -> QueryResponseItem:
    result = get_top_n_prediction(item, engines['engine'])

    return result


@app.post("/actor_info")
async def film_info(item: DetailsDataInItem) -> QueryResponseActorInfo:
    result = get_actor_info(item)

    return result


@app.post("/film_info")
async def film_info(item: DetailsDataInItem) -> QueryResponseFilmInfo:
    result = get_film_info(item)

    return result


@app.post("/top_box_office")
async def top_box_office(n: int) -> QueryResponseBoxOffice:
    result = get_top_n_box_office_films(n)

    return result

@app.post("/llm")
async def llm(item: LLMItem) -> LLMItem:
    result = predict_llm(item, engines['llm_engine'])

    return result


if __name__ == '__main__':
    uvicorn.run(app)
