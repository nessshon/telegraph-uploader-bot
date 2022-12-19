from contextlib import suppress

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted
from aiogram.utils.exceptions import MessageCantBeEdited, MessageToEditNotFound


async def edit_message(message: Message, text: str,
                       reply_markup: InlineKeyboardMarkup | None = None,
                       disable_web_page_preview: bool = None) -> Message:
    with suppress(MessageCantBeEdited, MessageToEditNotFound):
        return await message.edit_text(
            text, reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview
        )


async def delete_message(message: Message) -> None:
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


async def delete_previous_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    with suppress(KeyError, MessageCantBeDeleted, MessageToDeleteNotFound):
        message_id = data["message_id"]

        if message_id:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=data["message_id"]
            )


def waiting_previous_execution(func, *args, **kwargs):
    async def decorator(message: Message, state: FSMContext):
        user_data = await state.get_data()

        if 'throttling' in user_data and user_data['throttling']:
            raise CancelHandler()

        return await func(message, state, *args, **kwargs)

    return decorator


def rate_limit(limit: float, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)

        return func

    return decorator
