from aiogram.types import ChatType, Message
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):

    async def check(self, message: Message) -> bool:
        return ChatType.PRIVATE == message.chat.type
