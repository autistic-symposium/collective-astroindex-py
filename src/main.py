#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py

import argparse

from src.utils.plot import plot_collective
from src.intel.collective import CollectiveIndex


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='✨ AstroIDX I: Collective ✨')
    parser.add_argument('-a', dest='transit_daily', action='store_true',
                        help='Calculate index for transit_daily.')
    parser.add_argument('-b', dest='transit_monthly', action='store_true',
                        help='Calculate index for transit_monthly.')
    parser.add_argument('-c', dest='transit_natal_daily', action='store_true',  
                        help='Calculate index for transit_natal_daily.')    
    parser.add_argument('-d', dest='moon_phase', action='store_true',
                        help='Calculate index for moon_phase.')
    parser.add_argument('-e', dest='planet_tropical', action='store_true',
                        help='Calculate index for planet_tropical.')
    parser.add_argument('-f', dest='chart_data', action='store_true',
                        help='Calculate index for chart_data.')
    parser.add_argument('-g', dest='western_horoscope', action='store_true',
                        help='Calculate index for western_horoscope.')
    parser.add_argument('-nw', dest='natal_wheel', action='store_true',
                        help='Print natal wheel.')
    parser.add_argument('-ci', dest='collective_index', action='store_true',
                        help='Calculate total collective index.')
    return parser

def run() -> None:

    parser = run_menu()
    args = parser.parse_args()
    c = CollectiveIndex()

    if args.transit_daily:
        c.get_transits_daily()

    elif args.transit_monthly:
        c.get_transits_monthly()
    
    elif args.transit_natal_daily:
        c.get_transits_natal_daily()
    
    elif args.moon_phase:
        c.get_moon_phase()
    
    elif args.planet_tropical:
        c.get_planet_tropical()
    
    elif args.natal_wheel:
        c.get_natal_wheel()

    elif args.chart_data:
        c.get_chart_data()
    
    elif args.western_horoscope:
        c.get_western_horoscope()

    elif args.collective_index:
        c.get_collective_index()

    else:
        parser.print_help()


if __name__ == "__main__":
    run()
