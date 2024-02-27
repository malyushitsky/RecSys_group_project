import pandas as pd
from src.details.schemas import (
    QueryResponseBoxOffice,
    QueryResponseFilmInfo,
    ActorInfo,
    QueryResponseActorInfo,
)
from src.details.utils import box_office_validate, film_validate


MOVIES_PATH = "./data/initial_data/movie_metadata.csv"
ACTORS_PATH = "./data/initial_data/actors_metadata.csv"
BOX_OFFICE_COLS = ["Movie_name", "Movie_release_date_year", "Movie_box_office_revenue"]
FILM_COLS = [
    "Movie_name",
    "Movie_release_date_year",
    "Movie_runtime",
    "Movie_box_office_revenue",
]


def get_top_n_box_office_films(n):
    """
    Returns top n box office films

        Params:
                query (Dict): request query
                n (int): n for top

        Returns: final_query (Dict): output structure like QueryResponseItem class
    """
    df = pd.read_csv(MOVIES_PATH).sort_values(
        by=["Movie box office revenue"], ascending=False
    )
    df.columns = df.columns.str.replace(" ", "_")
    final_lst = []
    for i in range(n):
        try:
            cur_dct = {
                BOX_OFFICE_COLS[j]: df[BOX_OFFICE_COLS].values[i][j]
                for j in range(len(BOX_OFFICE_COLS))
            }
            film_obj = box_office_validate(cur_dct)
        except Exception as e:
            print(e)
        else:
            final_lst.append(film_obj)
    final_obj = QueryResponseBoxOffice(response=final_lst)

    return final_obj


def get_film_info(input_obj):
    """
    Returns movie information for their title

        Params:
                query (Dict): request query

        Returns: final_query (Dict): output structure like QueryResponseFilmInfo class
    """
    df = pd.read_csv(MOVIES_PATH)
    info = df[df["Movie name"].str.lower() == input_obj.query.lower()].copy()
    info.columns = info.columns.str.replace(" ", "_")
    final_lst = []
    for i in range(info.shape[0]):
        try:
            cur_dct = {
                FILM_COLS[j]: info[FILM_COLS].values[i][j]
                for j in range(len(FILM_COLS))
            }
            film_obj = film_validate(cur_dct)
        except Exception as e:
            print(e)
        else:
            final_lst.append(film_obj)
    final_obj = QueryResponseFilmInfo(query=input_obj.query, response=final_lst)

    return final_obj


def get_actor_info(input_obj):
    """
    Returns actor information for his name and surname

        Params:
                query (Dict): request query

        Returns: final_query (Dict): output structure like QueryResponseActorInfo class
    """
    df = pd.read_csv(ACTORS_PATH)
    info = df[df["Actor name"].str.lower() == input_obj.query.lower()].copy()
    info["Actor gender"] = info["Actor gender"].apply(
        lambda x: "Male" if x == "M" else "Female"
    )
    info_dict = {}
    try:
        info_dict["Actor_name"] = info["Actor name"].values[0]
        info_dict["Actor_gender"] = info["Actor gender"].values[0]
        info_dict["Actor_height"] = info["Actor height (in meters)"].values[0]
        info_dict["Actor_date_of_birth"] = info["Actor date of birth"].values[0]
    except (KeyError, IndexError):
        info_dict["Actor_name"] = "No data"
        info_dict["Actor_gender"] = "No data"
        info_dict["Actor_height"] = "No data"
        info_dict["Actor_date_of_birth"] = "No data"
    actor_obj = ActorInfo(**info_dict)
    final_obj = QueryResponseActorInfo(query=input_obj.query, response=actor_obj)

    return final_obj
