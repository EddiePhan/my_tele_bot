import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv
load_dotenv()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
API_TOKEN = os.getenv("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Store bot screaming status
screaming = False

# Pre-assign menu text
FIRST_MENU = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button."
SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."

# Pre-assign button text
NEXT_BUTTON = "Next"
BACK_BUTTON = "Back"
TUTORIAL_BUTTON = "Tutorial"

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=NEXT_BUTTON, callback_data=NEXT_BUTTON)]
])
SECOND_MENU_MARKUP = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton(text=TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")]
])

# @dp.message(~F.command)
# async def echo(message: types.Message):
#     """
#     This function handles messages coming from the Bot API
#     """
#     print(f'{message.from_user.first_name} wrote {message.text}')
#
#     if screaming and message.text:
#         await message.answer(
#             message.text.upper(),
#             entities=message.entities
#         )
#     else:
#         await message.copy_to(message.chat.id)

@dp.message(Command("scream"))
async def scream(message: types.Message):
    """
    This function handles the /scream command
    """
    global screaming
    screaming = True
    await message.reply("Screaming mode activated!")

@dp.message(Command("whisper"))
async def whisper(message: types.Message):
    """
    This function handles /whisper command
    """
    global screaming
    screaming = False
    await message.reply("Whispering mode activated.")

@dp.message(Command("menu"))
async def menu(message: types.Message):
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """
    await message.answer(
        FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )

@dp.callback_query(F.data.in_([NEXT_BUTTON, BACK_BUTTON]))
async def button_tap(callback_query: types.CallbackQuery):
    """
    This handler processes the inline buttons on the menu
    """
    if callback_query.data == NEXT_BUTTON:
        text = SECOND_MENU
        markup = SECOND_MENU_MARKUP
    elif callback_query.data == BACK_BUTTON:
        text = FIRST_MENU
        markup = FIRST_MENU_MARKUP

    await callback_query.answer()

    await callback_query.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )

async def main():
    # Start the bot
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
