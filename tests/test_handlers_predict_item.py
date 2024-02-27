from unittest.mock import patch
import asyncio
import pytest
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
import sys
sys.path.append('..')
from Telegram_bot.handlers.predict_item import cmd_one, query_chosen_one, query_chosen_incorrectly_one, \
    n_predictions_chosen_incorrectly_one, n_predictions_chosen_one
# from Telegram_bot.utils.server_funcs import ITEM_ENDPOINT


class Request(StatesGroup):
    query = State()
    n_predictions = State()


mocked_reply = "<u> For your query 'example query' we can recommend next movies: </u>\n\n<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n<b> Movie box office revenue: </b> $2,782,275,172\n\n"


@pytest.mark.asyncio
async def test_cmd_one():
    bot = MockedBot(MessageHandler(cmd_one, Command(commands=["rec"])))
    message = MESSAGE.as_object(text="/rec")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert answer == "Введите запрос:"


@pytest.mark.asyncio
async def test_query_chosen_one():
    bot = MockedBot(MessageHandler(query_chosen_one, state=Request.query))
    message = MESSAGE.as_object(text="valid query")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Спасибо. Теперь, пожалуйста, выберите количество рекомендаций:" in answer


@pytest.mark.asyncio
async def test_query_chosen_incorrectly_one():
    bot = MockedBot(MessageHandler(query_chosen_incorrectly_one, state=Request.query))
    message = MESSAGE.as_object(text="invalid")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Недопустимое значение." in answer


@pytest.mark.asyncio
async def test_n_predictions_chosen_incorrectly_one():
    bot = MockedBot(MessageHandler(n_predictions_chosen_incorrectly_one, state=Request.n_predictions))
    message = MESSAGE.as_object(text="invalid")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Недопустимое значение. Пожалуйста, выберите количество рекомендаций из списка ниже:" in answer


@pytest.mark.asyncio
@patch('Telegram_bot.handlers.predict_item.get_reply')
async def test_n_predictions_chosen_one(mock_get_reply):
    mock_get_reply.return_value = mocked_reply
    bot = MockedBot(MessageHandler(n_predictions_chosen_one, state=Request.n_predictions, state_data={'query': 'example query'}))
    calls = await bot.query(MESSAGE.as_object(text="5"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert messages.text == "<u> For your query 'example query' we can recommend next movies: </u>\n\n<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n<b> Movie box office revenue: </b> $2,782,275,172\n\n"



# def divide_list_into_equal_groups(input_list, num_groups):
#     min_group_size = len(input_list) // num_groups
#     num_larger_groups = len(input_list) % num_groups
#     divided_list = []
#     start = 0
#     for i in range(num_groups):
#         end = start + min_group_size + (i < num_larger_groups)
#         divided_list.append(input_list[start:end])
#         start = end
#     return divided_list


# Mocked response for get_reply to be used in our test

from unittest.mock import AsyncMock, Mock
# from Telegram_bot.utils.server_funcs import get_reply
from Telegram_bot.utils import server_funcs
# from Telegram_bot.handlers.predict_item import get_reply
# @pytest.fixture()
# def mock_get_reply(mocker):
#     async_mock = AsyncMock()
#     mocker.patch('Telegram_bot.handlers.predict_item.get_reply', side_effect=async_mock)
#     mocker.patch('Telegram_bot.utils.server_funcs.get_reply', side_effect=async_mock)
#     return async_mock
#
# @pytest.mark.asyncio
# async def test_get_reply(mock_get_reply):
#     mock_get_reply.return_value = mocked_reply
#     result = get_reply(ITEM_ENDPOINT, json={'n_recs': '5', 'query': 'example query'})
#     assert result == 2

from unittest.mock import AsyncMock, Mock
from Telegram_bot.utils import server_funcs

# @pytest.mark.asyncio
# @patch('Telegram_bot.utils.server_funcs.get_reply')
# # @patch('Telegram_bot.utils.server_funcs.get_reply', return_value=mocked_reply)
# async def test_get_reply(mock_get_reply):
#     mock_get_reply.return_value = mocked_reply
#     result = server_funcs.get_reply(ITEM_ENDPOINT, json={'n_recs': '5', 'query': 'example query'})
#     assert result == 2








# from unittest.mock import patch
# # from my_module import total_value
# from utils.server_funcs import get_reply
# mocked_reply = "<u> For your query 'example query' we can recommend next movies: </u>\n\n<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n<b> Movie box office revenue: </b> $2,782,275,172\n\n"
#
# # @patch('utils.server_funcs.get_reply', return_value=mocked_reply)
# @pytest.mark.asyncio
# @patch('utils.server_funcs.get_reply', return_value=mocked_reply)
# async def test_n_predictions_chosen_one():
#     # with patch('utils.server_funcs.get_reply') as get_reply:
#     #     get_reply.return_value = mocked_reply
#         bot = MockedBot(MessageHandler(n_predictions_chosen_one, state=Request.n_predictions, state_data={'query': 'example query'}))
#         calls = await bot.query(MESSAGE.as_object(text="1"))
#         messages = calls.send_message.fetchone().text
#         print('--?__', messages)
#         # assert '1' == messages
#         # assert len(mocked_reply) == len(get_reply.return_value)
#         get_reply.assert_called_with(mocked_reply)

# async def sum(x, y):
#     await asyncio.sleep(1)
#     return x + y


# # Замокиваем
# import pytest
# import asyncio
#
# @pytest.fixture()
# def mock_sum(mocker):
#     future = asyncio.Future()
#     future.set_result(4)
#     mocker.patch('tests_handlers_predict_item4.sum', return_value=future)
#
# # Вызываем
#
#
# @pytest.mark.asyncio
# async def test_sum(mock_sum):
#     result = await sum(1, 2)
#     # I know 1+2 is equal to 3 but one man can only dream!
#     assert result == 4
#
# from unittest.mock import AsyncMock
#
# @pytest.fixture()
# def mock_sum(mocker):
#     async_mock = AsyncMock(return_value=4)
#     mocker.patch('app.sum', side_effect=async_mock)



# -----------
# from unittest.mock import AsyncMock
#
# from Telegram_bot.utils.server_funcs import sum
#
# @pytest.fixture()
# def mock_sum(mocker):
#     async_mock = AsyncMock()
#     mocker.patch('Telegram_bot.utils.server_funcs.sum', side_effect=async_mock)
#     return async_mock
#
# @pytest.mark.asyncio
# async def test_sum(mock_sum):
#     mock_sum.return_value = 4
#     result = await sum(1, 2)
#     assert result == 2