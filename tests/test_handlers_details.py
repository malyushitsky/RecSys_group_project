
from unittest.mock import patch
import pytest
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
import sys
sys.path.append('..')
from Telegram_bot.handlers.details import cmd_settimer, cmd_actor, cmd_film


mocked_reply_topbox = """<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n<b> Movie box office revenue: </b> $2,782,275,172\n\n<b> Movie release date year: </b> 1997\n<b> Movie box office revenue: </b> $2,185,372,302'"""
mocked_reply_actor = """<b> Actor name: </b> Brad Pitt\n<b> Actor gender: </b> Male\n<b> Actor height: </b> 1.8\n<b> Actor date of birth: </b> 1963-12-18"""
mocked_reply_film = """<b> Movie name: </b> King Kong\n<b> Movie release date year: </b> 1976\n<b> Movie runtime: </b> 134\n<b> Movie box office revenue: </b> $90,614,445\n\n<b> Movie name: </b> King Kong\n<b> Movie release date year: </b> 1933\n<b> Movie runtime: </b> 100\n<b> Movie box office revenue: </b> $1,856,000\n\n<b> Movie name: </b> King Kong\n<b> Movie release date year: </b> 2005\n<b> Movie runtime: </b> 186\n<b> Movie box office revenue: </b> $550,500,000"""


@pytest.mark.asyncio
async def test_cmd_settimer_no_args():
    bot = MockedBot(MessageHandler(cmd_settimer, Command(commands=["topbox"])))
    message = MESSAGE.as_object(text="/topbox")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "После команды необходимо ввести количество фильмов" in answer


@pytest.mark.asyncio
async def test_cmd_settimer_invalid_number():
    bot = MockedBot(MessageHandler(cmd_settimer, Command(commands=["topbox"])))
    message = MESSAGE.as_object(text="/topbox abc")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Вводимый параметр после команды должен быть числом." in answer


@pytest.mark.asyncio
async def test_cmd_settimer_out_of_bounds():
    bot = MockedBot(MessageHandler(cmd_settimer, Command(commands=["topbox"])))
    # Test for less than 0
    message = MESSAGE.as_object(text="/topbox -1")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "ВВоди от 1 до 15" in answer
    # Test for more than 15
    message = MESSAGE.as_object(text="/topbox 20")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "ВВоди от 1 до 15" in answer


@pytest.mark.asyncio
@patch('Telegram_bot.handlers.details.get_reply')
async def test_settimer(mock_get_reply):
    mock_get_reply.return_value = mocked_reply_topbox
    bot = MockedBot(MessageHandler(cmd_settimer, Command(commands=["topbox"])))
    calls = await bot.query(MESSAGE.as_object(text="/topbox 2"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert messages.text == """<b> Movie name: </b> Avatar\n<b> Movie release date year: </b> 2009\n<b> Movie box office revenue: </b> $2,782,275,172\n\n<b> Movie release date year: </b> 1997\n<b> Movie box office revenue: </b> $2,185,372,302'"""


@pytest.mark.asyncio
async def test_cmd_actor_no_args():
    bot = MockedBot(MessageHandler(cmd_actor, Command(commands=["actor"])))
    message = MESSAGE.as_object(text="/actor")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "После команды необходимо ввести имя для поиска" in answer


@pytest.mark.asyncio
async def test_cmd_actor_bad_query():
    bot = MockedBot(MessageHandler(cmd_actor, Command(commands=["actor"])))
    message = MESSAGE.as_object(text="/actor Ab")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Ошибка: введи нормально" in answer


@pytest.mark.asyncio
@patch('Telegram_bot.handlers.details.get_reply')
async def test_md_actor(mock_get_reply):
    mock_get_reply.return_value = mocked_reply_actor
    bot = MockedBot(MessageHandler(cmd_actor, Command(commands=["actor"])))
    calls = await bot.query(MESSAGE.as_object(text="/actor Brad Pitt"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert messages.text == """<b> Actor name: </b> Brad Pitt\n<b> Actor gender: </b> Male\n<b> Actor height: </b> 1.8\n<b> Actor date of birth: </b> 1963-12-18"""


@pytest.mark.asyncio
async def test_cmd_film_no_args():
    bot = MockedBot(MessageHandler(cmd_film, Command(commands=["film"])))
    message = MESSAGE.as_object(text="/film")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "После команды необходимо ввести название для поиска" in answer


@pytest.mark.asyncio
async def test_cmd_film_bad_query():
    bot = MockedBot(MessageHandler(cmd_film, Command(commands=["film"])))
    message = MESSAGE.as_object(text="/film 1")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert "Ошибка: введи нормально" in answer


@pytest.mark.asyncio
@patch('Telegram_bot.handlers.details.get_reply')
async def test_md_actor(mock_get_reply):
    mock_get_reply.return_value = mocked_reply_film
    bot = MockedBot(MessageHandler(cmd_film, Command(commands=["film"])))
    calls = await bot.query(MESSAGE.as_object(text="/film  King Kong"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert messages.text == """<b> Movie name: </b> King Kong\n<b> Movie release date year: </b> 1976\n<b> Movie runtime: </b> 134\n<b> Movie box office revenue: </b> $90,614,445\n\n<b> Movie name: </b> King Kong\n<b> Movie release date year: </b> 1933\n<b> Movie runtime: </b> 100\n<b> Movie box office revenue: </b> $1,856,000\n\n<b> Movie name: </b> King Kong\n<b> Movie release date year: </b> 2005\n<b> Movie runtime: </b> 186\n<b> Movie box office revenue: </b> $550,500,000"""

