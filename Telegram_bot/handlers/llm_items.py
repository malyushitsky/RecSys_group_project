from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from utils.server_funcs import get_reply, LLM_ENDPOINT

router = Router()


class Request_LLm(StatesGroup):
    query = State()


@router.message(Command("llm"))
async def cmd_llm(message: Message, state: FSMContext):
    await message.answer("Введите запрос:")
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(Request_LLm.query)


@router.message(Request_LLm.query)
async def llm_reply(message: Message):
    reply = get_reply(LLM_ENDPOINT, json={"query": message.text})
    await message.answer(reply)
