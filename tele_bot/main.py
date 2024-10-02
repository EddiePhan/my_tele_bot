import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
load_dotenv()

# Replace 'YOUR_BOT_API_TOKEN' with your actual Telegram Bot API token
API_TOKEN = os.getenv("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Handler for the /start command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hello! I'm a simple Telegram bot. How can I help you?")

# Handler for regular text messages
@dp.message()
async def echo_message(message: types.Message):
    await message.answer(f"You said: {message.text}")

# Main function to start the bot
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
