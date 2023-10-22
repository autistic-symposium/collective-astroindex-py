# -*- encoding: utf-8 -*-
# src/utils/plot.py

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


FONT = {
            'family': 'serif',
            'color':  'darkred',
            'weight': 'normal',
            'size': 16,
        }


def plot_collective(data: dict, title):
    """Plot collective bullish index."""

    plt.title(title, fontdict=FONT)
    plt.xlabel('Date', fontdict=FONT)
    plt.ylabel('Index', fontdict=FONT)

    ordered_data = sorted(data.items(), key = lambda x: datetime.strptime(x[0], '%d-%m-%Y'))

    x, y = zip(*ordered_data) 
    plt.plot(x, y)
    plt.show()
