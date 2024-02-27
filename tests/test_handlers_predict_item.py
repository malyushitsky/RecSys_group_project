from unittest.mock import patch
import pytest
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
import sys

sys.path.append("..")
from Telegram_bot.handlers.predict_item import (  # noqa: E402
    cmd_one,
    query_chosen_one,
    query_chosen_incorrectly_one,
    n_predictions_chosen_incorrectly_one,
    n_predictions_chosen_one,
)


class Request(StatesGroup):
    query = State()
    n_predictions = State()


mocked_reply = ("<u> For your query 'example query' we can recommend next movies: </u>\n\n"
                "<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n"
                "<b> Movie box office revenue: </b> $2,782,275,172\n\n"
                )


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
    bot = MockedBot(
        MessageHandler(
            n_predictions_chosen_incorrectly_one, state=Request.n_predictions
        )
    )
    message = MESSAGE.as_object(text="invalid")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert (
        "Недопустимое значение. Пожалуйста, выберите количество рекомендаций из списка ниже:"
        in answer
    )


@pytest.mark.asyncio
@patch("Telegram_bot.handlers.predict_item.get_reply")
async def test_n_predictions_chosen_one(mock_get_reply):
    mock_get_reply.return_value = mocked_reply
    bot = MockedBot(
        MessageHandler(
            n_predictions_chosen_one,
            state=Request.n_predictions,
            state_data={"query": "example query"},
        )
    )
    calls = await bot.query(MESSAGE.as_object(text="5"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert (
        messages.text
        == "<u> For your query 'example query' we can recommend next movies: </u>\n\n"
           "<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n"
           "<b> Movie box office revenue: </b> $2,782,275,172\n\n"
    )
