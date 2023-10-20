#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py

import argparse

from src.utils.os import load_config
import src.astro.collective as astro


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='✨ Astro Index ✨')
    parser.add_argument('-c', dest='collective', action='store_true',
                        help='Forecast for collective for the week')
    return parser


def run() -> None:

    env_vars = load_config()
    parser = run_menu()
    args = parser.parse_args()

    if args.collective:
        astro.get_collective_forecast_today(env_vars)

    else:
        parser.print_help()


if __name__ == "__main__":
    run()
