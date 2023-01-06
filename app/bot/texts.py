from aiogram.types import User


class Text:
    strings = {
        "en": {
            "start": (
                "<b>Hi {}!</b>\n\n"
                "This bot will help you upload your files to "
                "telegra.ph and get links to them.\n\n"
                "<b>Upload your file:</b>\n"
                "<i>Only .jpg, .jpeg, .png, .gif and .mp4 files "
                "with a maximum size of 5 MB are allowed.</i>"
            ),
            "source": (
                "https://github.com/nessshon/telegraph-uploader-bot"
            ),
            "file_to_big_error": (
                "<b>File too big:{}</b>\n"
                "<i>The file size must not exceed 5 MB.</i>"
            ),
            "retry_after_error": (
                "<b>Flood control exceeded!</b>\n"
                "<i>Retry in {} seconds.</i>"
            ),
            "file_type_error": (
                "<b>Unsupported type!</b>\n"
                "<i>Allowed only .jpg, .jpeg, .png, .gif and .mp4 files.</i>"
            ),
            "another_error": (
                "<b>Unknown error!</b>\n"
                "<i>Try again later.</i>"
            ),
        },
        "ru": {
            "start": (
                "<b>Привет {}!</b>\n\n"
                "Этот бот поможет загрузить файлы в "
                "telegra.ph и получить на них ссылки.\n\n"
                "<b>Отправьте файл:</b>\n"
                "<i>Допускаются файлы .jpg, .jpeg, .png, .gif и .mp4 "
                "с максимальным размером 5 МБ.</i>"
            ),
            "source": (
                "https://github.com/nessshon/telegraph-uploader-bot"
            ),
            "file_to_big_error": (
                "<b>Файл слишком большой:{}</b>\n"
                "<i>Размер файла не должен превышать 5MB.</i>"
            ),
            "retry_after_error": (
                "<b>Превышено кол-во запросов!</b>\n"
                "<i>Повторите попытку через {} секунд.</i>"
            ),
            "file_type_error": (
                "<b>Неподдерживаемый тип!</b>\n"
                "<i>Разрешены только файлы .jpg, .jpeg, .png, .gif и .mp4.</i>"
            ),
            "another_error": (
                "<b>Неизвестная ошибка!</b>\n"
                "<i>Попробуйте повторить позже.</i>"
            )
        }
    }

    def __init__(self):
        language_code = User.get_current().language_code
        self.language_code = language_code if language_code == "ru" else "en"

    def get(self, key: str) -> str:
        return self.strings[self.language_code][key]
