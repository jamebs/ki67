import logging
from datetime import datetime
from functools import wraps

from magda.module import Module

from ki67.common import Request


def get_logger(ref: Module.Runtime):
    name = f'ki67.modules.{ref.__class__.__name__}.{ref.name}'
    logger = logging.getLogger(name)
    return logger


def log(ref: Module.Runtime, request: Request, msg: str):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prefix = (
        '\u001B[33m'
        f'[{now}] '
        '\u001B[34m'
        f'{ref.__class__.__name__} '
        '\u001B[1m'
        f'({ref.name})'
        '\u001B[35m'
        f'[{request.uid}]'
        '\u001B[22m\u001B[39m'
    )
    print(f'{prefix} - {msg}')


def with_logger(fn):
    @wraps(fn)
    def wrapper(ref: Module.Runtime, *args, **kwargs):
        request: Request = kwargs.get('request')
        log(ref, request, '\u001B[32m\u001B[1m[START]\u001B[22m\u001B[39m')
        return fn(ref, *args, **kwargs)
    return wrapper
