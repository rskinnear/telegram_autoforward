import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
from datetime import datetime
import json

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from logger import setup_logger
from shifts import get_shift_from_timestamp

load_dotenv()
TOKEN: str | None = os.getenv("BOT_TOKEN")
GROUP_USERNAME: str = ""

dp = Dispatcher()

logger = setup_logger(name="auto_forward", log_file="auto_forward.log")


async def read_cm_data():
    """
    Reads cm data from json file
    """
    with open("cm_data.json", "r", encoding="utf-8") as file:
        cm_data = json.load(file)

    return cm_data


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}! I will listen to messages in the Telegram group and forward them here."
    )

    if message.from_user:
        await update_user_chat_id(message.from_user)


async def update_user_chat_id(user: types.User):
    """
    Adds the user_id key to the cm_data.json file
    """
    cm_data = await read_cm_data()
    changed = False
    for cm_info in cm_data["cms"]["jaguars"].values():
        if cm_info["username"] == user.username.lower() and "chat_id" not in cm_info:
            cm_info["chat_id"] = user.id
            changed = True

    if changed:
        with open("cm_data.json", "w") as file:
            json.dump(cm_data, file, indent=4)


async def get_cm_on_shift(message_timestamp: datetime) -> int | None:
    """
    Fetches the chat_id for the CM on shift given the current timestamp
    """
    current_shift = get_shift_from_timestamp(message_timestamp=message_timestamp)

    try:
        cm_data = await read_cm_data()

        for cm_name, cm_info in cm_data["cms"]["jaguars"].items():
            if cm_info["shift"] == current_shift:
                return cm_info["chat_id"]

    except Exception as e:
        logger.error(f"Error while fetching CM: {e}")

    logger.error("Couldn't find a CM to forward message to.")
    return None


@dp.message()
async def forward_to_user(message: types.Message):
    """
    Forward the telegram message to the CM on shift
    """
    logger.info(
        f"Message received: {message.text} from {message.from_user.username} in {message.chat.username}"
    )
    # Check if the message is from the specific chat username
    if message.chat.username != GROUP_USERNAME:
        return  # Ignore message if it's not from the specific chat username

    # Check if the message is from a bot
    if message.from_user.is_bot:
        return  # Ignore message if it's from a bot

    try:
        cm_on_shift = await get_cm_on_shift(message.date)
        if cm_on_shift:
            await message.forward(cm_on_shift)
    except Exception as e:
        logger.exception(f"Error encountered: {e}")


async def main() -> None:
    """
    Initializes the Telegram bot.
    """
    if TOKEN:
        # Initialize Bot instance with a default parse mode which will be passed to all API calls
        bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
        # And the run events dispatching
        await dp.start_polling(bot)
        logger.info("Bot is running.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
