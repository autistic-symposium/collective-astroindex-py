# -*- encoding: utf-8 -*-
# src/utils/plot.py

import matplotlib.pyplot as plt
import numpy as np


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

    lists = sorted(data.items())
    x, y = zip(*lists) 
    plt.plot(x, y)
    plt.show()
