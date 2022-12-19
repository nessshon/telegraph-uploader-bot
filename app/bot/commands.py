import asyncio

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, BotCommand,
                           BotCommandScopeAllPrivateChats)

from aiogram.utils import markdown
from aiogram.dispatcher.filters import CommandStart

from .texts import Text
from .filters import IsPrivate
from .misc import (rate_limit, edit_message,
                   delete_previous_message, delete_message)


@rate_limit(2.2)
async def command_start(message: Message, state: FSMContext):
    emoji = await message.answer("👋")

    await delete_previous_message(message, state)
    await delete_message(message)
    await asyncio.sleep(2)

    user_link = markdown.hlink(
        title=message.from_user.first_name,
        url=message.from_user.url
    )
    text = Text(message.from_user.language_code).get("start")

    await edit_message(emoji, text.format(user_link))
    async with state.proxy() as data:
        data.clear()
    await state.update_data(message_id=emoji.message_id)


@rate_limit(2.2)
async def command_source(message: Message, state: FSMContext):
    emoji = await message.answer("👨‍💻")

    await delete_previous_message(message, state)
    await delete_message(message)
    await asyncio.sleep(2)

    text = Text(message.from_user.language_code).get("source")
    await edit_message(emoji, text)
    await state.update_data(message_id=emoji.message_id)


async def setup(bot: Bot):
    commands = {
        "en": [
            BotCommand("start", "Restart"),
            BotCommand("source", "Source code")
        ],
        "ru": [
            BotCommand("start", "Перезапустить"),
            BotCommand("source", "Исходный код")
        ]
    }

    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru"
    )
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )


def register(dp: Dispatcher):
    dp.register_message_handler(
        command_start, IsPrivate(), CommandStart()
    )
    dp.register_message_handler(
        command_source, IsPrivate(), commands="source"
    )
