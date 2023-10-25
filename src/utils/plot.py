# -*- encoding: utf-8 -*-
# src/utils/plot.py


from datetime import datetime
import matplotlib.pyplot as plt


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

    ordered_data = sorted(data.items(), key = lambda x: datetime.strptime(x[0], '%d-%m-%Y'))
    x, y = zip(*ordered_data) 
    
    plt.plot(x, y)
    plt.show()
