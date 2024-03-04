import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from aggregation import aggregate_salary
from config import settings

bot = Bot(token=settings.bot_token)

dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Отправьте даты")


@dp.message()
async def echo(message: types.Message):
    query = await aggregate_salary(message.text)
    message_max_sz = 4096
    len_query = len(str(query))
    if len_query > message_max_sz:
        for x in range(0, len_query, message_max_sz):
            await bot.send_message(message.from_user.id, str(query)[x:x+message_max_sz])
    else:
        await bot.send_message(message.from_user.id, str(query))


async def main():
    await dp.start_polling(bot)


asyncio.run(main())