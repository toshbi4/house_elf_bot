import asyncio
import logging
import re

from aiogram import Bot, Dispatcher, types, executor
import random

f = open("bot_token.txt", "r")
BOT_TOKEN = f.read().strip()
f.close()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Id of users, who can use this bot.
admins_id = 0
verified_users_id = 0
newbee_code = 0

f = open("verified_users.txt", "r")
lines = f.read()
verified_users_id = list(map(int, lines.split()))
f.close()
print('verified_users_id: ', verified_users_id)

f = open("admins.txt", "r")
lines = f.read()
admins_id = list(map(int, lines.split()))
f.close()
print('admins_id: ', admins_id)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """

    await message.answer(f"Hi! {message.from_user.first_name}! 👋",
                         parse_mode=types.ParseMode.HTML,
                         )


@dp.message_handler(commands=['invite_code'])
async def newbee_req(message: types.Message):
    global newbee_code, verified_users_id

    print(message.text[13:17])
    if newbee_code == 0:
        await message.answer(f"Попроси админа выдать тебе код регистрации.")
    elif newbee_code == int(message.text[13:17]):
        newbee_code = 0

        verified_users_id.append(message.from_user.id)
        f = open("verified_users.txt", "a")
        f.write(f"{message.from_user.id}")
        f.close()
        print('verified_users_id: ', verified_users_id)

        await message.answer(f"Добро пожаловать в наши ряды, боец!")
    else:
        await message.answer(f" Ты че, Мыш!.")


@dp.message_handler(commands=['new'], user_id=admins_id)
async def add_new_verified(message: types.Message):
    global newbee_code

    newbee_code = random.randint(1000, 9999)
    print(newbee_code)
    await message.answer(f"Код для новенького: {newbee_code}")


@dp.message_handler()
async def echo(message: types.Message):
    global verified_users_id

    if message.from_user.id in verified_users_id:
        await message.answer("Я тебя знаю, ты ровный пацан!")
    else:
        await message.answer(" Кыш отседова. Чмо!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
