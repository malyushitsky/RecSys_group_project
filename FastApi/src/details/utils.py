from src.details.schemas import BoxOfficeItem, FilmInfo

# from schemas import BoxOfficeItem, FilmInfo


def isNAN(x):
    return x != x


def box_office_validate(input_dct):
    dct = input_dct.copy()
    dct_new = {}
    for key in dct:
        # Movie_name
        if key == "Movie_name":
            if isinstance(dct[key], str) and not isNAN(dct[key]):
                dct_new[key] = dct[key]
            else:
                dct_new[key] = "No data"
        # Movie_release_date_year
        if key == "Movie_release_date_year":
            if (isinstance(dct[key], float) or isinstance(dct[key], int)) and not isNAN(dct[key]):
                dct_new[key] = int(dct[key])
            else:
                dct_new[key] = "No data"
        # Movie_box_office_revenue
        if key == "Movie_box_office_revenue":
            if (isinstance(dct[key], float) or isinstance(dct[key], int)) and not isNAN(dct[key]):
                dct_new[key] = int(dct[key])
            else:
                dct_new[key] = "No data"

    obj = BoxOfficeItem(**dct_new)

    return obj


def film_validate(input_dct):
    dct = input_dct.copy()
    dct_new = {}
    for key in dct:
        # Movie_name
        if key == "Movie_name":
            if isinstance(dct[key], str) and not isNAN(dct[key]):
                dct_new[key] = dct[key]
            else:
                dct_new[key] = "No data"
        # Movie_release_date_year
        if key == "Movie_release_date_year":
            if (isinstance(dct[key], float) or isinstance(dct[key], int)) and not isNAN(dct[key]):
                dct_new[key] = int(dct[key])
            else:
                dct_new[key] = "No data"
        # Movie_runtime
        if key == "Movie_runtime":
            if (isinstance(dct[key], float) or isinstance(dct[key], int)) and not isNAN(dct[key]):
                dct_new[key] = int(dct[key])
            else:
                dct_new[key] = "No data"
        # Movie_box_office_revenue
        if key == "Movie_box_office_revenue":
            if (isinstance(dct[key], float) or isinstance(dct[key], int)) and not isNAN(dct[key]):
                dct_new[key] = int(dct[key])
            else:
                dct_new[key] = "No data"

    obj = FilmInfo(**dct_new)

    return obj
