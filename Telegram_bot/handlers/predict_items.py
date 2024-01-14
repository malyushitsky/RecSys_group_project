

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.kb1 import make_row_keyboard
from utils.filters import check_query
from utils.server_funcs import get_reply, ITEMS_ENDPOINT, divide_list_into_equal_groups, MAX_MESSAGE_LEN


router = Router()
available_n_predictions = [str(i) for i in range(1, 6)]


class Request_items(StatesGroup):
    query = State()
    n_predictions = State()


@router.message(Command("batch_rec"))
async def cmd_more(message: Message, state: FSMContext):
    await message.answer("Введите запросы (разделитель - ;):")
    await state.set_state(Request_items.query)


@router.message(StateFilter(Request_items.query), F.text.func(lambda x: check_query(x)))
async def query_chosen_more(message: Message, state: FSMContext):
    await state.update_data(query=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите количество рекомендаций (для каждого запроса):",
        reply_markup=make_row_keyboard(available_n_predictions)
    )
    await state.set_state(Request_items.n_predictions)


@router.message(StateFilter(Request_items.query))
async def query_chosen_incorrectly_more(message: Message):
    await message.answer(
        text="Недопустимое значение. Запрос может быть длиной от 10 до 100 символов и "
             "содержать только буквы, цифры, пробелы и символы ,.-;"
    )


@router.message(Request_items.n_predictions, F.text.in_(available_n_predictions))
async def n_predictions_chosen_more(message: Message, state: FSMContext):
    user_data = await state.get_data()
    queries = [{'n_recs': message.text, 'query': q.strip()} for q in user_data['query'].split(';')]
    reply = get_reply(ITEMS_ENDPOINT, json={"objects": queries})
    if len(reply) > MAX_MESSAGE_LEN:
        n_split = (len(reply) // MAX_MESSAGE_LEN) + 1
        splitted_reply = divide_list_into_equal_groups(reply.split('\n\n'), n_split)
        for rep in splitted_reply:
            await message.answer(
                text='\n\n'.join(rep),
                reply_markup=ReplyKeyboardRemove(),
                parse_mode='HTML'
            )
    else:
        await message.answer(
            text=reply,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='HTML'
        )
    await state.clear()


@router.message(StateFilter(Request_items.n_predictions))
async def n_predictions_chosen_incorrectly_more(message: Message):
    await message.answer(
        text="Недопустимое значение. Пожалуйста, выберите количество рекомендаций из списка ниже:",
        reply_markup=make_row_keyboard(available_n_predictions)
    )
