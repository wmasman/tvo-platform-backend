import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class DirectusError(Exception):
    pass


class InvalidBaseUrlError(DirectusError):
    pass


class MissingAuthTokenError(DirectusError):
    pass


class InvalidFileParamsError(DirectusError):
    pass


class FileDownloadError(DirectusError):
    pass
