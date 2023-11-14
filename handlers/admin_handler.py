from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import URLInputFile
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from keyboard import approve, back, main_kb
from states import St
from film_tools import film_scraper, helper
from film_tools.film_builder import build_film
from db.db import DB
from random import randint as rand

router = Router()
router.callback_query.middleware(CallbackAnswerMiddleware())
db = DB()

with open('admins.txt', 'r') as admin_file:
    admins = admin_file.read().split(',')
    print(f'Admin list: {", ".join(admins)}')


@router.message(Command("films"))
async def get_films(msg: Message, state: FSMContext):
    if str(msg.from_user.id) in admins:
        films = db.get_keysfilms()
        answer = ''
        for i in films:
            answer += f'{i[1]}: {i[3]}\n'
        await msg.answer(f'Найдено: {len(films)}\n{answer}')



@router.message(Command("add"))
async def url_enter(msg: Message, state: FSMContext):
    await state.set_state(St.add)
    if str(msg.from_user.id) in admins:
        await msg.answer('👽 Введите ссылку (film.ru): ', reply_markup=back)
        await state.set_state(St.url)


@router.message(Command("help"))
async def url_enter(msg: Message, state: FSMContext):
    await state.set_state(St.add)
    if str(msg.from_user.id) in admins:
        await msg.answer('/add - Добавить фильм\n/films - Посмотреть список всех фильмов и кодов к ним')



@router.message(St.url)
async def url_add(msg: Message, state: FSMContext):
    url = msg.text
    
    try:
        data = await film_scraper.get_filminfo(url)
    except Exception as e:
        await msg.answer(f'Произошла ошибка при добавлении фильма: {e}')

    film_img = URLInputFile(data['image'])
    film_info = (data["name"], data["duration"], data["score"], data["genre"], data["year"], data["country"], data["desc"])
    film_msg = await msg.answer_photo(film_img, caption=build_film(*film_info), reply_markup=approve)
    image_id = film_msg.photo[-1].file_id


    @router.callback_query(F.data == 'accept')
    async def accept_film(msg: Message):
        key = rand(1000, 9999)
        try:
            db.add_film(key, image_id, *film_info)
            await msg.answer(f'✅ Фильм был успешно добавлен под кодом: {key}!', reply_markup=main_kb)
            await state.set_state(St.main)
        except Exception as e:
            await msg.answer(f'🚫 Произошла ошибка при добавлении фильма: {e}!', reply_markup=main_kb)
            await state.set_state(St.main)


@router.callback_query(F.data == 'reject')
async def accept_film(msg: Message, state: FSMContext):
    await msg.answer('🚫 Отмена...', reply_markup=main_kb)
    await state.set_state(St.main)


@router.callback_query(F.data == 'change')
async def accept_film(msg: Message, state: FSMContext):
    await msg.answer('В разработке.', reply_markup=main_kb)
    await state.set_state(St.main)
    # реализация редактирования...

