import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import predict_item, details, predict_items, llm_items
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import F
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)

dp.include_router(predict_item.router)
dp.include_router(details.router)
dp.include_router(predict_items.router)
dp.include_router(llm_items.router)


@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Бот поможет подобрать фильм по описанию. Хотите рекомендацию по: "
        "1 фильму (/rec) или нескольким (/batch_rec) ?",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message(StateFilter(None), Command(commands=["cancel"]))
@dp.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(text="Нечего отменять", reply_markup=ReplyKeyboardRemove())


@dp.message(Command(commands=["cancel"]))
@dp.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Отменено. Можем начать заново", reply_markup=ReplyKeyboardRemove()
    )


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/help", description="Справка по работе бота"),
        BotCommand(
            command="/cancel", description="Отмена обработки в командах, ожидающих ввод"
        ),
        BotCommand(command="/rec", description="Рекомендации по описанию"),
        BotCommand(
            command="/batch_rec", description="Рекомендации по нескольким описаниям"
        ),
        BotCommand(command="/topbox", description="Топ фильмов по кассовым сборам"),
        BotCommand(command="/actor", description="Краткая информация об актере"),
        BotCommand(command="/film", description="Краткая информация о фильме"),
        BotCommand(command="/llm", description="Рекомендации по описанию от LLm"),
    ]

    await bot.set_my_commands(main_menu_commands)


async def main():
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
