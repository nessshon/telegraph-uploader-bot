import asyncio
import io
import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from .texts import Text
from .filters import IsPrivate
from .misc import edit_message, waiting_previous_execution, rate_limit

from ..telegraph.api import Telegraph
from ..telegraph.exceptions import (TelegraphException, RetryAfterError,
                                    FileTypeError, FileEmptyError, FileToBigError)

ALLOWED_CONTENT_TYPES = [
    ContentType.PHOTO, ContentType.VIDEO, ContentType.VIDEO_NOTE,
    ContentType.DOCUMENT, ContentType.ANIMATION
]


@rate_limit(2.2)
@waiting_previous_execution
async def message_upload(message: Message, state: FSMContext):
    if message.content_type in ALLOWED_CONTENT_TYPES:
        telegraph = Telegraph()
        file, file_size = io.BytesIO(), 0

        emoji = await message.reply("⌛️")
        await state.update_data(throttling=True)

        try:
            if message.content_type == ContentType.PHOTO:
                file = await message.photo[-1].download(destination_file=file)

            elif message.content_type == ContentType.VIDEO:
                file = await message.video.download(destination_file=file)

            elif message.content_type == ContentType.VIDEO_NOTE:
                file = await message.video_note.download(destination_file=file)

            elif message.content_type == ContentType.ANIMATION:
                file = await message.animation.download(destination_file=file)

            elif message.content_type == ContentType.DOCUMENT:
                file = await message.document.download(destination_file=file)

            uploaded = await telegraph.upload_file(file.getbuffer())
            await edit_message(emoji, uploaded.url, disable_web_page_preview=True)

        except FileToBigError as e:
            await edit_message(emoji, "🤨")
            await asyncio.sleep(2)

            file_size = e.__str__().split(":")[1]
            text = Text().get("file_to_big_error")
            await emoji.edit_text(text.format(file_size))

        except RetryAfterError as e:
            await edit_message(emoji, "😴")
            await asyncio.sleep(2)

            seconds = re.match(r"\d+", e.__str__())
            text = Text().get("retry_after_error")
            await emoji.edit_text(text.format(seconds))

        except (FileTypeError, FileEmptyError):
            await edit_message(emoji, "🙄")
            await asyncio.sleep(2)

            text = Text().get("file_type_error")
            await emoji.edit_text(text)

        except TelegraphException:
            await edit_message(emoji, "❗️")
            await asyncio.sleep(2)

            text = Text().get("another_error")
            await emoji.edit_text(text)

        finally:
            await state.update_data(throttling=False)

    else:
        emoji = await message.reply("🙄")
        await asyncio.sleep(2)

        text = Text().get("file_type_error")
        await edit_message(emoji, text)


def register(dp: Dispatcher):
    dp.register_message_handler(
        message_upload, IsPrivate(),
        content_types=ContentType.ANY
    )
