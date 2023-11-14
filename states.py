from aiogram.fsm.state import StatesGroup, State


class St(StatesGroup):
    main = State()
    code = State()
    add = State()
    url = State()