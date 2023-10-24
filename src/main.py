#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py

import argparse

from src.utils.os import load_config
from src.utils.plot import plot_collective
from src.intel.collective import CollectiveIndex


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='✨ AstroIDX I: Collective ✨')
    parser.add_argument('-ct', dest='collective_today', action='store_true',
                        help='Forecast for the collective today.')
    parser.add_argument('-cm', dest='collective_monthly', action='store_true',
                        help='Forecast for the collective this month.')
    parser.add_argument('-cc', dest='collective_custom', action='store_true',
                        help='Forecast for the collective in a custom date range.')
    parser.add_argument('-m', dest='moon', action='store_true',
                        help='Moon phase.')
    parser.add_argument('-c', dest='collective', action='store_true',
                        help='Forecast for the collective (all intel).')
    parser.add_argument('-t', dest='transit', action='store_true',
                        help='Transit forecast.')
    parser.add_argument('-w', dest='wheel', action='store_true',
                        help='Wheel forecast.')
    parser.add_argument('-cd', dest='chart_data', action='store_true',
                        help='Chart data.') 
    parser.add_argument('-ws', dest='whole_sign', action='store_true',
                        help='Whole sign houses.')
    parser.add_argument('-n', dest='natal', action='store_true',
                        help='Natal chart.')
    return parser

def run() -> None:

    env_vars = load_config()
    parser = run_menu()
    args = parser.parse_args()
    PRINT_PLOT = False
    c = CollectiveIndex(env_vars)

    # TODO: Add argument for city and country
    if args.collective_today:
        c.get_transits_daily()

    elif args.collective_monthly:
        c.get_collective_forecast_monthly()
        # TODO: remove plot from here, add option to save/name
        if PRINT_PLOT:
            plot_collective(c.transit_index, "Collective Transit Index (monthly))")
    
    elif args.collective_custom:
        c.get_collective_forecast_custom()
        # TODO: remove plot from here, add option to save/name
        if PRINT_PLOT:
            plot_collective(c.transit_index, "Collective Transit Index (daily))")
    
    elif args.moon:
        c.get_collective_forecast_moon()
        if PRINT_PLOT:
            plot_collective(c.moon_phase, "Moon Phase")
    
    elif args.transit:
        c.get_transit_forecast()
    
    elif args.collective:
        c.get_collective_forecast_today()
        c.get_collective_forecast_monthly()
        c.get_collective_forecast_custom()
        c.get_collective_forecast_moon()
        # TODO: how is this being added/used?
        c.get_transit_forecast()
        # TODO: add whole sign houses
        plot_collective(c.transit_index, "Collective Transit Index (all intel))")
        
    elif args.wheel:
        c.get_wheel()

    elif args.chart_data:
        c.get_chart_data()
    
    elif args.whole_sign:
        c.get_whole_sign_houses()
    
    elif args.natal:
        # TODO: this does not work
        c.get_natal_chart()

    else:
        parser.print_help()


if __name__ == "__main__":
    run()
