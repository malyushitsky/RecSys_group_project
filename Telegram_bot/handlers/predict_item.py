

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards.kb1 import make_row_keyboard
from keyboards.kb2 import create_pagination_keyboard
from utils.filters import check_query
from utils.server_funcs import get_reply, ITEM_ENDPOINT, divide_list_into_equal_groups, MAX_MESSAGE_LEN


router = Router()
available_n_predictions = [str(i) for i in range(1, 11)]


class Request(StatesGroup):
    query = State()
    n_predictions = State()


@router.message(Command("rec"))
async def cmd_one(message: Message, state: FSMContext):
    await message.answer("Введите запрос:")
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(Request.query)


@router.message(StateFilter(Request.query), F.text.func(lambda x: check_query(x)))
async def query_chosen_one(message: Message, state: FSMContext):
    await state.update_data(query=message.text.lower())
    await message.answer(
        text="Спасибо. Теперь, пожалуйста, выберите количество рекомендаций:",
        reply_markup=make_row_keyboard(available_n_predictions)
    )
    await state.set_state(Request.n_predictions)


@router.message(StateFilter(Request.query))
async def query_chosen_incorrectly_one(message: Message):
    await message.answer(
        text="Недопустимое значение. Запрос может быть длиной от 10 до 100 символов и "
             "содержать только буквы, цифры, пробелы и символы ,.-;"
    )


@router.message(Request.n_predictions, F.text.in_(available_n_predictions))
async def n_predictions_chosen_one(message: Message, state: FSMContext):
    user_data = await state.get_data()
    reply = get_reply(ITEM_ENDPOINT, json={"n_recs": message.text, "query": user_data['query']})
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
    # Сброс состояния и сохранённых данных у пользователя
    await state.clear()



# Заготовка под книжку - мб в будушем

# @router.message(Request.n_predictions, F.text.in_(available_n_predictions))
# async def n_predictions_chosen(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     url_main = 'http://127.0.0.1:8000'
#     req = {"query": user_data['query']}
#     cur_req = requests.post(url_main + '/predict_item', json=req).json()
#     await message.answer(
#         # text=str(cur_req.get('response')[0]),
#         text='\n'.join([f"{key}:{cur_req.get('response')[0][key]}" for key in cur_req.get('response')[0]]),
#         reply_markup=create_pagination_keyboard(
#             'backward',
#             f"1/{len(cur_req.get('response'))}",
#             'forward'
#         )
#     )
#
#
# @router.callback_query(F.data == 'forward')
# async def process_forward_press(callback: CallbackQuery):
#     # if users_db[callback.from_user.id]['page'] < len(book):
#     #     users_db[callback.from_user.id]['page'] += 1
#     #     text = book[users_db[callback.from_user.id]['page']]
#     await callback.message.edit_text(
#         text='Нужно тоже куда-то сохранять результат запроса',
#         reply_markup=create_pagination_keyboard(
#                 'backward',
#                 f'2/2',
#                 'forward'
#             )
#         )
#     await callback.answer()


@router.message(StateFilter(Request.n_predictions))
async def n_predictions_chosen_incorrectly_one(message: Message):
    await message.answer(
        text="Недопустимое значение. Пожалуйста, выберите количество рекомендаций из списка ниже:",
        reply_markup=make_row_keyboard(available_n_predictions)
    )