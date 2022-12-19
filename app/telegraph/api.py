import logging

import aiohttp
import secrets

from . import config
from .types import File
from .exceptions import (TelegraphException, RetryAfterError,
                         FileTypeError, FileEmptyError, FileToBigError)


class Telegraph:

    def __init__(self):
        self.base_url = config.BASE_URL

    async def upload_file(self, file: memoryview) -> File:
        """
        Allowed only .jpg, .jpeg, .png, .gif and .mp4 files.

        :param file: memoryview
        """
        form = aiohttp.FormData(quote_fields=False)
        form.add_field(secrets.token_urlsafe(8), file)

        async with aiohttp.ClientSession() as session:
            response = await session.post(url=self.base_url.format(
                endpoint="upload"), data=form)
            json_response = await response.json()

            if isinstance(json_response, list):
                error = json_response[0].get('error')
            else:
                error = json_response.get('error')

            if error:
                if isinstance(error, str) and "flood" in error.lower():
                    raise RetryAfterError(error)

                elif isinstance(error, str) and error.startswith("File type invalid"):
                    raise FileTypeError(error)

                elif isinstance(error, str) and error.startswith("File too big"):
                    raise FileToBigError(error)

                elif isinstance(error, str) and error.startswith("File empty"):
                    raise FileEmptyError(error)

                else:
                    logging.error(error)
                    raise TelegraphException(error)

            return [File(**obj) for obj in json_response][0]
