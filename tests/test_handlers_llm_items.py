from unittest.mock import patch
import pytest
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram_tests import MockedBot
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import MESSAGE
import sys

sys.path.append("..")
from Telegram_bot.handlers.llm_items import cmd_llm, llm_reply  # noqa: E402


class Request(StatesGroup):
    query = State()
    n_predictions = State()


mocked_reply = (
    "\nBased on the context information provided, here are three dystopian films:\n\n"
    "1. Fortress (1993) - Set in a dystopian future, this film follows a couple who are "
    "caught trying to cross the US-Canada border and sentenced to a private maximum security "
    "prison. The prison is located over a deep pit and is run by a corporation that uses "
    "technology to control the inmates. The film explores themes of government control, "
    "human rights, and the consequences of a one-child policy.\n\n"
    "2. Until the End of the World (1991) - This film takes place in late 1999, when a nuclear "
    "satellite is about to reenter the atmosphere and cause a massive panic. The main character, "
    "Claire, escapes the traffic jam and encounters a hitchhiker who is traveling around the world "
    "to gather images for a secret research project. The film explores themes of memory, identity, "
    "and the power of technology.\n\n"
    "3. 1984 (1984) - Based on George Orwell's novel, this film is set in a totalitarian superstate "
    "where the main character, Winston Smith, works in the Ministry of Truth and secretly keeps a "
    "diary of his private thoughts. The film explores themes of government control, censorship, and "
    "the dangers of totalitarianism.\n"
)


@pytest.mark.asyncio
async def test_cmd_llm():
    bot = MockedBot(MessageHandler(cmd_llm, Command(commands=["llm"])))
    message = MESSAGE.as_object(text="/llm")
    calls = await bot.query(message)
    answer = calls.send_message.fetchone().text
    assert answer == "Введите запрос:"


@pytest.mark.asyncio
@patch("Telegram_bot.handlers.llm_items.get_reply")
async def test_llm_reply(mock_get_reply):
    mock_get_reply.return_value = mocked_reply
    bot = MockedBot(
        MessageHandler(
            llm_reply,
            state=Request.n_predictions,
            state_data={"query": "example query"},
        )
    )
    calls = await bot.query(MESSAGE.as_object(text="5"))
    messages = calls.send_message.fetchone()
    assert len(messages.text) > 0
    assert (
        messages.text
        == ("\nBased on the context information provided, here are three dystopian films:\n\n"
            "1. Fortress (1993) - Set in a dystopian future, this film follows a couple who are "
            "caught trying to cross the US-Canada border and sentenced to a private maximum security "
            "prison. The prison is located over a deep pit and is run by a corporation that uses "
            "technology to control the inmates. The film explores themes of government control, "
            "human rights, and the consequences of a one-child policy.\n\n"
            "2. Until the End of the World (1991) - This film takes place in late 1999, when a nuclear "
            "satellite is about to reenter the atmosphere and cause a massive panic. The main character, "
            "Claire, escapes the traffic jam and encounters a hitchhiker who is traveling around the world "
            "to gather images for a secret research project. The film explores themes of memory, identity, "
            "and the power of technology.\n\n"
            "3. 1984 (1984) - Based on George Orwell's novel, this film is set in a totalitarian superstate "
            "where the main character, Winston Smith, works in the Ministry of Truth and secretly keeps a "
            "diary of his private thoughts. The film explores themes of government control, censorship, and "
            "the dangers of totalitarianism.\n"
            )
    )
