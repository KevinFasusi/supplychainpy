# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pickle
import re
import logging
import time

from functools import wraps

from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_DASH

UNKNOWN = 'UNKNOWN'


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
        with open(ABS_FILE_PATH_DASH, 'wb') as f:
            pickle.dump(state_map, f)
        return message

    return wrapper


def keyword_sniffer(func):
    @wraps(func)
    def wrapper(**kwargs):
        temp_kwargs = {}
        temp_kwargs.update({'file_path': kwargs.get('file_path', UNKNOWN),
                            'df': kwargs.get('df', UNKNOWN),
                            'raw_data': kwargs.get('raw_data', UNKNOWN),
                            'file_type': kwargs.get('file_type', UNKNOWN),
                            'retail_price': kwargs.get('raw_data', UNKNOWN),
                            'quantity_on_hand': kwargs.get('quantity_on_hand', UNKNOWN),
                            'sku': kwargs.get('sku_id', UNKNOWN),
                            'lead_time': kwargs.get('lead_time', UNKNOWN),
                            'unit_cost': kwargs.get('unit_cost', UNKNOWN),
                            'currency': kwargs.get('currency', UNKNOWN)
                            })
        return func(**temp_kwargs)

    return wrapper


def coroutine_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        coroutine.next()
        return coroutine

    return wrapper


def pickle_conifg(func):
    @wraps(func)
    def wrapper(**kwargs):
        with open(kwargs['file_path'], 'wb') as f:
            pickle.dump(kwargs['config'], f)
