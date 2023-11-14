from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from handlers import admin_handler, basic_handler
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import St
from aiogram.filters import Command
from db.db import DB
from keyboard import main_kb, sub
from tools.check_sub import check_sub
from aiogram import F


dp = Dispatcher()
dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.include_routers(admin_handler.router, basic_handler.router)
db = DB()


@dp.message(St.main)
@dp.message(Command("start"))
async def start(msg: Message, state:FSMContext):
    name = msg.from_user.first_name
    userid = msg.from_user.id
    subbed = await check_sub(userid)
    if subbed:
        if db.get_user(userid) is None:
            db.add_user(userid)
            print(f'[INF] New user #{userid} has been succesfully added to database!')
        await msg.answer(f'🥳 Добро пожаловать, {name}!'
                        '\nДля навигации воспользуйтесь кнопками.',
                         reply_markup=main_kb)
        await state.clear()
    else:
        await msg.answer(f'🥳 Добро пожаловать, {name}!'
                        '\nПожалуйста, подпишитесь на канал'
                        '\n<a href="https://t.me/fevertt">Movies Fever</a>, чтобы использовать функции бота.',
                         parse_mode='HTML')


@dp.message(F.text == "↩️ Отмена")
async def cancel(msg: Message, state: FSMContext):
    await start(msg, state)