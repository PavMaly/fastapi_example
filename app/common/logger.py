import functools
import logging
import sys
import traceback

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='[%(levelname)s]  %(asctime)s >> %(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler]


def log_error_with_traceback(e: Exception):
    logging.error(e.__repr__())
    logging.error(f'Traceback: {traceback.format_tb(e.__traceback__)}')


def log(func):
    msg = func.__qualname__

    @functools.wraps(func)
    def deco(*args, **kwargs):
        response = func(*args, **kwargs)
        logger.debug(msg)
        logger.info(response)
        return response
    return deco
