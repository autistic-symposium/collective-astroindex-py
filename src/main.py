#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py

import argparse

from src.utils.os import load_config
from src.intel.collective import Collective


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='✨ Choices ✨')
    parser.add_argument('-cn', dest='collective_now', action='store_true',
                        help='Forecast for the collective now.')
    return parser

def run() -> None:

    env_vars = load_config()
    parser = run_menu()
    args = parser.parse_args()

    # TODO: Add argument for city and country
    if args.collective_now:
        c = Collective(env_vars)
        c.get_collective_forecast_now()

    else:
        parser.print_help()


if __name__ == "__main__":
    run()
