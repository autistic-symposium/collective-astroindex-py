# -*- encoding: utf-8 -*-
# utils/os.py

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from pprint import PrettyPrinter



def set_logging(log_level) -> None:
    """Set logging level according to .env config."""

    if log_level == 'INFO' or log_level == 'info':
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    elif log_level == 'ERROR' or log_level == 'error':
        logging.basicConfig(level=logging.ERROR, format='%(message)s')

    elif log_level == 'DEBUG' or log_level == 'debug':
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    else:
        print(f'Logging level {log_level} is not available. Setting to ERROR')
        logging.basicConfig(level=logging.ERROR, format='%(message)s')


def load_config() -> dict:
    """Load and set environment variables."""

    env_file = Path('.') / '.env'
    if not os.path.isfile(env_file):
        exit_with_error('Please create an .env file')

    env_vars = {}
    load_dotenv(env_file)

    try:
        env_vars['API_KEY'] = os.getenv('API_KEY')
        env_vars['USER_ID'] = os.getenv('USER_ID')
        env_vars['API_URL'] = os.getenv('API_URL')
        set_logging(os.getenv('LOG_LEVEL'))

        return env_vars

    except KeyError as e:
        exit_with_error(f'Cannot extract env variables: {e}. Exiting.')


def log_error(string) -> None:
    """Print STDOUT error using the logging library."""

    logging.error('🚨 %s', string)


def log_info(string) -> None:
    """Print STDOUT info using the logging library."""

    logging.info('✨ %s', string)


def log_debug(string) -> None:
    """Print STDOUT debug using the logging library."""

    logging.debug('🟨 %s', string)


def exit_with_error(message) -> None:
    """Log an error message and halt the program."""

    log_error(message)
    sys.exit(1)


def pprint(data: dict, indent=None) -> None:
    """Print dicts and data in a suitable format"""

    print()
    indent = indent or 4
    pp = PrettyPrinter(indent=indent)
    pp.pprint(data)
    print()