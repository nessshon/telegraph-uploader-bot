class TelegraphException(Exception):
    ...


class RetryAfterError(TelegraphException):
    ...


class FileTypeError(TelegraphException):
    ...


class FileEmptyError(TelegraphException):
    ...


class FileToBigError(TelegraphException):
    ...
