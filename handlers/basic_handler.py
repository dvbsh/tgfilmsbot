from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram.fsm.context import FSMContext
from states import St
from aiogram import F
from db.db import DB
from film_tools.film_builder import build_film
import asyncio
from keyboard import back, main_kb, sub
from aiogram.methods import GetChatMember
from tools.check_sub import check_sub
from bot import bot


router = Router()
router.callback_query.middleware(CallbackAnswerMiddleware())
db = DB()

not_subbed ='😶‍🌫️ Эта функция доступна только подписчикам. \n \nПожалуйста, подпишитесь на канал\n<a href="https://t.me/fevertt">Movies Fever</a>, чтобы использовать бота.'


@router.message(F.text == "✏️ Ввести код")
async def code_enter(msg: Message, state: FSMContext):
    subbed = await check_sub(msg.from_user.id)
    if subbed:
        await msg.answer('👀 Введите код фильма.', reply_markup=back)
        await state.set_state(St.code)
    else:
        await msg.answer(not_subbed, parse_mode='HTML', reply_markup=sub)


@router.message(St.code)
async def get_film(msg: Message, state: FSMContext):
    subbed = await check_sub(msg.from_user.id)
    if subbed:
        code = msg.text
        await msg.answer(f'🔍 Поиск фильма по коду {code}...')
        await asyncio.sleep(1)
        if code.isdigit() and  1000 < int(code) < 9999:
            code = int(code)
            film = db.get_film(code)
            if film:
                await asyncio.sleep(1)
                await msg.answer_photo(film[2], caption=(f'🗝 Код: {code}\n') + build_film(film[3], film[4], film[5],  film[6], film[7], film[8], film[9]), reply_markup=main_kb)
                await state.clear()
            else:
                await asyncio.sleep(1)
                await msg.answer(f'😵‍💫 Не удалось найти фильм с кодом "{code}".', reply_markup=back)
        else:
            await msg.answer('🫥 Неверный формат кода. Введите код ещё раз.', reply_markup=back)
    else:
        await msg.answer(not_subbed, parse_mode='HTML', reply_markup=sub)

    


@router.message(F.text == "❔️ Случайный фильм")
async def random_film(msg: Message, state: FSMContext):
    subbed = await check_sub(msg.from_user.id)
    if subbed:
        await msg.answer('🔍 Идёт поиск случайного фильма...')
        await asyncio.sleep(3)
        await msg.answer('🤩 Предлагаем вам посмотреть этот фильм!')
        await asyncio.sleep(1)
        randfilm = db.get_randfilm()
        await msg.answer_photo(randfilm[2], caption=(f'🗝 Код: {randfilm[1]}\n') + build_film(randfilm[3], randfilm[4], randfilm[5],  randfilm[6], randfilm[7], randfilm[8], randfilm[9]), reply_markup=main_kb)
        #добавить отметку "просмотрено"
    else:
        await msg.answer(not_subbed, parse_mode='HTML', reply_markup=sub)


@router.callback_query(F.data == "checksub")
async def check(msg: Message):
    subbed = await check_sub(msg.from_user.id)
    if subbed:
        await msg.answer('❤️', reply_markup=main_kb)
        await bot.send_message(msg.from_user.id, '🎉 Поздравляем! Теперь вам доступны все функции!')
    else:
        await bot.send_message(msg.from_user.id, '😭 Вы не являетесь участником канала.')

