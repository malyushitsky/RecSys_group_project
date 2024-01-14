

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from utils.filters import check_query
from utils.server_funcs import get_reply, BOX_OFFICE_ENDPOINT, ACTOR_ENDPOINT,FILM_ENDPOINT


router = Router()
# max message length = 4098


@router.message(Command("topbox"))
async def cmd_settimer(
        message: Message,
        command: CommandObject
):
    # no args
    if command.args is None:
        await message.answer(
            text="После команды необходимо ввести количество фильмов\nНапример /topbox <b> 4 </b>",
            parse_mode='HTML'
        )
        return
    # not num args
    try:
        top_n = int(command.args)
    except ValueError:
        await message.answer(
            "Вводимый параметр после команды должен быть числом. Пример:\n"
            "/topbox <b> 4 </b>"
        )
        return
    # bounds
    if top_n < 0 or top_n > 15:
        await message.answer("ВВоди от 1 до 15")
        return
    # output
    reply = get_reply(BOX_OFFICE_ENDPOINT, params={'n': top_n})
    # for i in range(3):
    await message.answer(
            text=reply,
            parse_mode='HTML'
        )


@router.message(Command("actor"))
async def cmd_actor(
        message: Message,
        command: CommandObject
):
    # no args
    if command.args is None:
        await message.answer(
            text="После команды необходимо ввести имя для поиска\nНапример /actor <b> Brad Pitt </b>",
            parse_mode='HTML'
        )
        return
    # bad query
    if not check_query(command.args, 4):
        await message.answer("Ошибка: введи нормально")
        return
    # output
    reply = get_reply(ACTOR_ENDPOINT, json={'query': command.args})
    await message.answer(
            text=reply,
            parse_mode='HTML'
        )


@router.message(Command("film"))
async def cmd_actor(
        message: Message,
        command: CommandObject
):
    # no args
    if command.args is None:
        await message.answer(
            text="После команды необходимо ввести название для поиска\nНапример /film <b> King Kong </b>",
            parse_mode='HTML'
        )
        return
    # bad query
    if not check_query(command.args, 1):
        await message.answer("Ошибка: введи нормально")
        return
    # output
    reply = get_reply(FILM_ENDPOINT, json={'query': command.args})
    await message.answer(
        text=reply,
        parse_mode='HTML'
    )