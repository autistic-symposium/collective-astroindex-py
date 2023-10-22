#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py

import argparse

from src.utils.os import load_config
from src.utils.plot import plot_collective
from src.intel.collective import Collective


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='✨ Choices ✨')
    parser.add_argument('-ct', dest='collective_today', action='store_true',
                        help='Forecast for the collective today.')
    parser.add_argument('-cm', dest='collective_monthly', action='store_true',
                        help='Forecast for the collective this month.')
    return parser

def run() -> None:

    env_vars = load_config()
    parser = run_menu()
    args = parser.parse_args()

    # TODO: Add argument for city and country
    if args.collective_today:
        c = Collective(env_vars)
        c.get_collective_forecast_today()

    if args.collective_monthly:
        c = Collective(env_vars)
        c.get_collective_forecast_monthly()
        plot_collective(c.transit_monthly_index, "Collective Transit Index")

    else:
        parser.print_help()


if __name__ == "__main__":
    run()
