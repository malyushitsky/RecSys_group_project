import requests

URL_MAIN = "http://127.0.0.1:8000"
BOX_OFFICE_ENDPOINT = "/top_box_office"
ACTOR_ENDPOINT = "/actor_info"
FILM_ENDPOINT = "/film_info"
ITEM_ENDPOINT = "/predict_item"
ITEMS_ENDPOINT = "/predict_items"
LLM_ENDPOINT = "/llm"
MAX_MESSAGE_LEN = 4098

# user_data = {'query': 'A World War 2 film'}
# user_data = {'query': 'A New Year Film'}


def divide_list_into_equal_groups(input_list, num_groups):
    # Рассчитываем минимальный размер каждой группы
    min_group_size = len(input_list) // num_groups
    # Рассчитываем количество групп, которые имеют на один элемент больше
    num_larger_groups = len(input_list) % num_groups
    # Делим список на группы равного или равного+1 размера
    divided_list = []
    start = 0
    for i in range(num_groups):
        end = start + min_group_size + (i < num_larger_groups)
        divided_list.append(input_list[start:end])
        start = end
    return divided_list


def process_reply(input_dict):
    html_text = ""
    if len(input_dict) != 0:
        for key in input_dict:
            if key == "Movie_box_office_revenue":
                rev = input_dict.get(key, "No data")
                if rev != "No data":
                    html_text += f"<b> {key.replace('_', ' ')}: </b> {'${:,.0f}'.format(input_dict[key])}\n"
                else:
                    html_text += f"<b> {key.replace('_', ' ')}: </b> {rev}\n"
            elif key == "Actor_height":
                html_text += f"<b> {key.replace('_', ' ')}: </b> {input_dict.get(key, 'No data')}\n"
            elif key == "text":
                html_text += f"<b> Synopsis: </b> {input_dict.get(key, 'No data')}\n"
            elif isinstance(input_dict.get(key, "No data"), list):
                html_text += f"<b> {key.replace('_', ' ')}: </b> {', '.join(input_dict.get(key, 'No data'))}\n"
            elif isinstance(input_dict.get(key, "No data"), float):
                html_text += f"<b> {key.replace('_', ' ')}: </b> {int(input_dict.get(key, 'No data'))}\n"
            else:
                html_text += f"<b> {key.replace('_', ' ')}: </b> {input_dict.get(key, 'No data')}\n"
        html_text += "\n"
    else:
        html_text += "NO DATA\n"

    return html_text


def get_reply(endpoint, json=None, params=None):
    error_fl = False
    try:
        server_reply = requests.post(
            URL_MAIN + endpoint, params=params, json=json
        ).json()
    except Exception as e:
        print("ERORR: ", e)
        error_fl = True
    if not error_fl:
        final_html = ""
        if endpoint in [BOX_OFFICE_ENDPOINT, FILM_ENDPOINT]:
            for query in server_reply["response"]:
                final_html += process_reply(query)
                # final_html += '\n'
        elif endpoint == ACTOR_ENDPOINT:
            final_html += process_reply(server_reply["response"])
        elif endpoint == ITEM_ENDPOINT:
            final_html += (f"<u> For your query '{json.get('query', 'No data')}' we can "
                           "recommend next movies: </u>\n\n")
            for query in server_reply["response"]:
                final_html += process_reply(query)
        elif endpoint == LLM_ENDPOINT:
            final_html += server_reply["query"]
        else:
            for obj in server_reply["objects"]:
                final_html += (
                    f"<u> For your query '{obj.get('query', 'No data')}' "
                    f"we can recommend next movies: </u>\n\n"
                )
                for query in obj["response"]:
                    final_html += process_reply(query)
    else:
        final_html = "<b>Что-то пошло не так :(</b>"

    return final_html
