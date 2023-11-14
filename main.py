import logging
import asyncio
from aiogram.filters import Command
from dispatcher import dp
from bot import bot


logging.basicConfig(level=logging.INFO)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())