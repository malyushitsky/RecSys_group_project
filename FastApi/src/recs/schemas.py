from pydantic import BaseModel
from typing import List, Union


class DataInItem(BaseModel):
    n_recs: int
    query: str


class DataIn(BaseModel):
    objects: List[DataInItem]


class FilmItem(BaseModel):
    Movie_name: str
    Movie_release_year: Union[int, str]
    Movie_runtime: Union[int, str]
    Movie_languages: str
    Movie_genres: str
    text: str


class QueryResponseItem(BaseModel):
    n_recs: int
    query: str
    response: List[FilmItem]


class DataOut(BaseModel):
    objects: List[QueryResponseItem]
