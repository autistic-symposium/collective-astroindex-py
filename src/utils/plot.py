# -*- encoding: utf-8 -*-
# src/utils/plot.py

import matplotlib.pyplot as plt
from src.utils.os import convert_date_format 


FONT = {
            'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
        }


def plot_collective(data: dict) -> None:

    plt.xlabel('Date', fontdict=FONT)
    plt.ylabel('Normalized Index', fontdict=FONT)
    plt.title('Collective Astro Index I', fontdict=FONT)

    ordered_data = sorted(data.items(), key = lambda x: convert_date_format(x[0]))
    x, y = zip(*ordered_data) 
    
    plt.plot(x, y)
    plt.show()
