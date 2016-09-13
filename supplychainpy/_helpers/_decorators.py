import os
import pickle
import re
import logging
import time

from functools import wraps

APP_DIR = os.path.dirname(__file__, )
REL_PATH = 'dash.pickle'
REL_PATH_CONFIG = 'config.pickle'
ABS_FILE_PATH = os.path.abspath(os.path.join(APP_DIR, '..', REL_PATH))
ABS_FILE_PATH_CONFIG = os.path.abspath(os.path.join(APP_DIR, '..', REL_PATH_CONFIG))


def log_this(level, name=None, message=None):
    """Logs and reports the execution time of methods and functions"""

    def time_this(func):
        logname = name if name else func.__module__
        log = logging.getLogger(__name__)
        log.addHandler(logging.NullHandler())
        log_msg = message if message else ''

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            log.log(level, 'Name of function called: {} Execution time for function: {} MESSAGE: {}'
                    .format(func.__name__, end - start, log_msg))
            return result

        return wrapper

    return time_this


def preprocess_text(func):
    """ Cleans up messy pronouns

    Args:
        func:

    Returns:

    """
    @wraps(func)
    def wrapper(*args):
        i_regex = re.compile('[iI][ ]')
        iam_regex = re.compile('[iI][\'][mM]')
        im_regex = re.compile('[iI][mM]')
        cleaned = []
        words = args[1].split(' ')
        for word in words:
            if i_regex.match(word):
                cleaned.append('I')
            elif iam_regex.match(word):
                cleaned.append("I am")
            elif im_regex.match(word):
                cleaned.append("I am")
            else:
                cleaned.append(word)
        message = ' '.join(cleaned)
        args = (args[0], message)
        return func(*args)

    return wrapper


def strip_punctuation(func):
    @wraps(func)
    def wrapper(*args):
        word = str(args[1])
        args = (args[0], word.strip('.'))
        return func(*args)
    return wrapper


def pickle_response(func):
        @wraps(func)
        def wrapper(*args):
            message = func(*args)
            state_map = {'last_utterance': message}
            with open(ABS_FILE_PATH , 'wb') as f:
                    pickle.dump(state_map, f)

            return message
        return wrapper
