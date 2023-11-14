from aiogram import types



main_kb = types.ReplyKeyboardMarkup(
        keyboard=[
        [types.KeyboardButton(text="✏️ Ввести код")],
        [types.KeyboardButton(text="❔️ Случайный фильм")]
        ],
        resize_keyboard=True
        )


back = types.ReplyKeyboardMarkup(
        keyboard=[
        [types.KeyboardButton(text="↩️ Отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
        )

sub = types.InlineKeyboardMarkup(
        inline_keyboard=[
        [types.InlineKeyboardButton(text="⚡️ Подписаться", url=f"https://t.me/private_bsq")],
        [types.InlineKeyboardButton(text="☑️ Проверить подписку", callback_data='checksub')]
        ]
        )



add = types.InlineKeyboardMarkup(
        inline_keyboard=[
        [types.InlineKeyboardButton(text="✍️ Вручную", callback_data='handed')],
        [types.InlineKeyboardButton(text="🔗 Ввести ссылку", callback_data='url')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
        )



approve = types.InlineKeyboardMarkup(
        inline_keyboard=[
    [types.InlineKeyboardButton(text="✅ Подтвердить ",callback_data="accept")],
    [types.InlineKeyboardButton(text="🚫 Отмена", callback_data="reject")],
    [types.InlineKeyboardButton(text="🖍 Изменить", callback_data="change")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
        )

