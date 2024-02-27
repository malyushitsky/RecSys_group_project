from pydantic import BaseModel
from typing import List, Union


class DetailsDataInItem(BaseModel):
    query: str


class FilmInfo(BaseModel):
    Movie_name: str
    Movie_release_date_year: Union[int, str]
    Movie_runtime: Union[int, float, str]
    Movie_box_office_revenue: Union[float, int, str]


class ActorInfo(BaseModel):
    Actor_name: str
    Actor_gender: Union[int, str]
    Actor_height: Union[int, float, str]
    Actor_date_of_birth: Union[str]


class BoxOfficeItem(BaseModel):
    Movie_name: str
    Movie_release_date_year: Union[int, str]
    Movie_box_office_revenue: Union[float, int, str]


class QueryResponseFilmInfo(BaseModel):
    query: str
    response: List[FilmInfo]


class QueryResponseActorInfo(BaseModel):
    query: str
    response: ActorInfo


class QueryResponseBoxOffice(BaseModel):
    response: List[BoxOfficeItem]
