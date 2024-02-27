import requests_mock
import sys

sys.path.append("..")
from Telegram_bot.utils.server_funcs import (  # noqa: E402
    divide_list_into_equal_groups,
    process_reply,
    get_reply,
)


def test_divide_list_into_equal_groups():
    input_list = [1, 2, 3, 4, 5, 6, 7, 8]
    num_groups = 3
    expected_output = [[1, 2, 3], [4, 5, 6], [7, 8]]
    result = divide_list_into_equal_groups(input_list, num_groups)
    assert result == expected_output

    input_list = []
    num_groups = 2
    expected_output = [[], []]
    result = divide_list_into_equal_groups(input_list, num_groups)
    assert result == expected_output


def test_process_reply():
    input_dict = {
        "Movie_box_office_revenue": 1000000,
        "Actor_height": 180,
        "text": "Sample synopsis",
    }
    expected_output = ("<b> Movie box office revenue: </b> $1,000,000\n<b> Actor height: "
                       "</b> 180\n<b> Synopsis: </b> Sample synopsis\n\n")
    result = process_reply(input_dict)
    assert result == expected_output


def test_get_reply_with_mock():
    with requests_mock.Mocker() as m:
        mock_response = {
            "response": [
                {"Movie_name": "Test Movie", "Movie_box_office_revenue": 500000}
            ]
        }
        m.post("http://127.0.0.1:8000/top_box_office", json=mock_response)
        endpoint = "/top_box_office"
        expected_html = "<b> Movie name: </b> Test Movie\n<b> Movie box office revenue: </b> $500,000\n\n"
        result = get_reply(endpoint)
        assert expected_html in result
