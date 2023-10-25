# -*- encoding: utf-8 -*-
# utils/os.py

import os
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from pprint import PrettyPrinter


def load_config() -> dict:
    """Load and set environment variables."""

    env_file = Path('.') / '.env'
    if not os.path.isfile(env_file):
        exit_with_error('Please create an .env file')

    env_vars = {}
    load_dotenv(env_file)

    try:
        set_logging(os.getenv('LOG_LEVEL'))
        global REQUIRED_FORMAT_STR
        REQUIRED_FORMAT_STR = os.getenv('REQUIRED_FORMAT_STR')

        env_vars['API_KEY'] = os.getenv('API_KEY')
        env_vars['USER_ID'] = os.getenv('USER_ID')
        env_vars['API_URL'] = os.getenv('API_URL')

        env_vars['STRATEGIES_GENERAL'] = os.getenv('STRATEGIES_GENERAL')
        env_vars['STRATEGIES_COLLECTIVE'] = os.getenv('STRATEGIES_COLLECTIVE')
        env_vars['STRATEGIES_RANKING'] = os.getenv('STRATEGIES_RANKING')
        env_vars['STRATEGIES_PLANETS_ASPECTS'] = os.getenv('STRATEGIES_PLANETS_ASPECTS')

        return env_vars

    except KeyError as e:
        exit_with_error(f'Cannot extract env variables: {e}. Exiting.')


def set_logging(log_level: str) -> None:
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


def load_yaml(path: str) -> dict:
    """Load yaml file from path."""

    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    except FileNotFoundError as e:
        exit_with_error(f'Cannot find file {path}: {e}. Exiting.')

    except yaml.YAMLError as e:
        exit_with_error(f'Cannot parse file {path}: {e}. Exiting.')


def log_error(string: str) -> None:
    """Print STDOUT error using the logging library."""

    logging.error('🚨 %s', string)


def log_info(string: str) -> None:
    """Print STDOUT info using the logging library."""

    logging.info('✨ %s', string)


def log_debug(string: str) -> None:
    """Print STDOUT debug using the logging library."""

    logging.debug('🟨 %s', string)


def exit_with_error(message: str) -> None:
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


def convert_date_format(date: str) -> str:
    """Convert date format to YYYY-MM-DD"""
    
    try:
        date = datetime.strptime(date, REQUIRED_FORMAT_STR)
    except ValueError as e:
        try:
            date = datetime.strptime(date, '%d-%m-%Y')
        except ValueError as e:
            try:
                date = datetime.strptime(date, '%m-%d-%Y')
            except ValueError as e:
                exit_with_error(f'Cannot parse date {date}: {e}. Exiting.')

    return date.strftime(REQUIRED_FORMAT_STR)


def get_middle_datetime(start_date: str, end_date: str) -> str:
    """Get the middle date between two dates."""

    start_date = datetime.strptime(start_date,REQUIRED_FORMAT_STR)
    end_date = datetime.strptime(end_date, REQUIRED_FORMAT_STR)
    middle_date = start_date + (end_date - start_date) / 2
    return middle_date.strftime(REQUIRED_FORMAT_STR)