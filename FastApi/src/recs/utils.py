from src.recs.schemas import FilmItem


def isNAN(x):
    return x != x


def preprocess_response(response, text):
    dct = response.copy()
    dct.update({"text": text})
    dct_new = {}
    for key in dct:
        # Movie_name
        if key == "Movie_name":
            if isinstance(dct[key], str) and not isNAN(dct[key]):
                dct_new[key] = dct[key]
            else:
                dct_new[key] = "No data"
        # Movie_release_year
        if key == "Movie_release_year":
            if isinstance(dct[key], int) and not isNAN(dct[key]):
                dct_new[key] = dct[key]
            else:
                dct_new[key] = "No data"
        # Movie_runtime
        if key == "Movie_runtime":
            if (isinstance(dct[key], float) or isinstance(dct[key], int)) and not isNAN(dct[key]):
                dct_new[key] = int(dct[key])
            else:
                dct_new[key] = "No data"
        # Movie_languages
        if key == "Movie_languages":
            if (
                isinstance(dct[key], list)
                and not isNAN(dct[key])
                and len(dct[key]) != 0
            ):
                dct_new[key] = ", ".join(dct[key])
            else:
                dct_new[key] = "No data"
        # Movie_genres
        if key == "Movie_genres":
            if (
                isinstance(dct[key], list)
                and not isNAN(dct[key])
                and len(dct[key]) != 0
            ):
                dct_new[key] = ", ".join(dct[key])
            else:
                dct_new[key] = "No data"
        # Movie_genres
        if key == "text":
            if isinstance(dct[key], str) and not isNAN(dct[key]):
                dct_new[key] = dct[key][:500]
            else:
                dct_new[key] = "No data"

    obj = FilmItem(**dct_new)

    return obj
