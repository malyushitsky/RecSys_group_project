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
from Telegram_bot.handlers.predict_items import cmd_more, query_chosen_more, query_chosen_incorrectly_more, \
    n_predictions_chosen_incorrectly_more, n_predictions_chosen_more


class Request(StatesGroup):
    query = State()
    n_predictions = State()


mocked_reply = """<u> For your query 'magic' we can recommend next movies: </u>\n\n<b> Movie name: </b> Magic Journeys\n<b> Movie release year: </b> 1982\n<b> Movie runtime: </b> 16\n<b> Movie languages: </b> English Language\n<b> Movie genres: </b> Short Film, Fantasy\n<b> Synopsis: </b> Magic Journeys looked at the world through the eyes of a child. The film started with children running through a meadow and looking at clouds. Someone blew on a dandelion and the seeds then flew away, turning into stars and then turned into the sun. Next the kids were seen flying a kite at the beach. The kite then turned into a bird, a fish, a school of fish, a flock of birds, bird wings, a Pegasus, a horse and then finally into a merry-go-round. While the children rode the carousel, they began\n\n<u> For your query 'dystopian' we can recommend next movies: </u>\n<b> Movie name: </b> Fortress\n<b> Movie release year: </b> 1993\n<b> Movie runtime: </b> 95\n<b> Movie languages: </b> English Language\n<b> Movie genres: </b> World cinema, Science Fiction, Indie, Dystopia\n<b> Synopsis: </b> Set in a dystopian future, 2017, ex-army officer John Henry Brennick  and his wife Karen  are attempting to cross the US-Canada border to Vancouver to have a second child. Strict one-child policies forbid a second pregnancy, but the couple believe they are justified because their first child died at birth. Brennick is caught  and sentenced to 31 years in a private maximum security prison run by the "MenTel Corporation". To maintain discipline all inmates are implanted with "Intestinators" which\n\n"""


@pytest.mark.asyncio
async def test_cmd_more():
    bot = MockedBot(MessageHandler(cmd_more, Command(commands=["batch_rec"])))
    message = MESSAGE.as_object(text="/batch_rec")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert answer == "Введите запросы (разделитель - ;):"


@pytest.mark.asyncio
async def test_query_chosen_more():
    bot = MockedBot(MessageHandler(query_chosen_more, state=Request.query))
    message = MESSAGE.as_object(text="valid query")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Спасибо. Теперь, пожалуйста, выберите количество рекомендаций (для каждого запроса):" in answer


@pytest.mark.asyncio
async def test_query_chosen_incorrectly_more():
    bot = MockedBot(MessageHandler(query_chosen_incorrectly_more, state=Request.query))
    message = MESSAGE.as_object(text="invalid")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Недопустимое значение." in answer


@pytest.mark.asyncio
async def test_n_predictions_chosen_incorrectly_more():
    bot = MockedBot(MessageHandler(n_predictions_chosen_incorrectly_more, state=Request.n_predictions))
    message = MESSAGE.as_object(text="invalid")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Недопустимое значение. Пожалуйста, выберите количество рекомендаций из списка ниже:" in answer


@pytest.mark.asyncio
@patch('Telegram_bot.handlers.predict_items.get_reply')
async def test_n_predictions_chosen_more(mock_get_reply):
    mock_get_reply.return_value = mocked_reply
    bot = MockedBot(MessageHandler(n_predictions_chosen_more, state=Request.n_predictions, state_data={'query': 'example query'}))
    calls = await bot.query(MESSAGE.as_object(text="1"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert messages.text == """<u> For your query 'magic' we can recommend next movies: </u>\n\n<b> Movie name: </b> Magic Journeys\n<b> Movie release year: </b> 1982\n<b> Movie runtime: </b> 16\n<b> Movie languages: </b> English Language\n<b> Movie genres: </b> Short Film, Fantasy\n<b> Synopsis: </b> Magic Journeys looked at the world through the eyes of a child. The film started with children running through a meadow and looking at clouds. Someone blew on a dandelion and the seeds then flew away, turning into stars and then turned into the sun. Next the kids were seen flying a kite at the beach. The kite then turned into a bird, a fish, a school of fish, a flock of birds, bird wings, a Pegasus, a horse and then finally into a merry-go-round. While the children rode the carousel, they began\n\n<u> For your query 'dystopian' we can recommend next movies: </u>\n<b> Movie name: </b> Fortress\n<b> Movie release year: </b> 1993\n<b> Movie runtime: </b> 95\n<b> Movie languages: </b> English Language\n<b> Movie genres: </b> World cinema, Science Fiction, Indie, Dystopia\n<b> Synopsis: </b> Set in a dystopian future, 2017, ex-army officer John Henry Brennick  and his wife Karen  are attempting to cross the US-Canada border to Vancouver to have a second child. Strict one-child policies forbid a second pregnancy, but the couple believe they are justified because their first child died at birth. Brennick is caught  and sentenced to 31 years in a private maximum security prison run by the "MenTel Corporation". To maintain discipline all inmates are implanted with "Intestinators" which\n\n"""