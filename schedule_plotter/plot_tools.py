# -*- coding: utf-8 -*-
"""
    plot_tools.py
    Functions to create and eventually show the plot
"""

__author__ = "giulpig"
__license__ = "GPLv3"

import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from schedule_plotter.Algorithm import Algorithm, Process
from typing import List, Tuple, Dict


# algo must be of Algorithm type and data must be an array of Processes
def test_schedule_algorithm(algo: Algorithm, to_schedule: List[Process]) -> None:
    print(f"Plotting {algo.name} algorithm")

    # Get the plot object
    ax = get_plot(algo, to_schedule)

    # I can manipulate the plot and show it
    ax.set_xlabel(algo.name)
    plt.show()


def get_plot(algo: Algorithm, to_schedule: List[Process], delta=0.4) -> matplotlib.figure.Figure:
    """:return: a drawing that you can manipulate, show, save etc"""

    # Run algorithm against Process list to create scheduled data
    scheduled_data = algo.function(to_schedule)

    yspan = len(scheduled_data)
    yplaces = [.5+i for i in range(yspan)]
    ylabels = sorted(scheduled_data.keys(), key=lambda name: int(name[1:]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_yticks(yplaces)
    ax.set_yticklabels(ylabels)
    ax.set_ylim((0,yspan))

    low, hi =  scheduled_data[ylabels[0]][0]
    for pos, label in zip(yplaces,ylabels):
        for (start, end) in scheduled_data[label]:
            ax.add_patch(patches.Rectangle((start,pos-delta/2.0),end-start,delta))
            if start<low : low=start
            if end>hi : hi=end

    # Draw an invisible line so that the x axis limits are automatically adjusted
    ax.plot((low,hi),(0,0))

    xmin, xmax = ax.get_xlim()
    ax.hlines(range(1,yspan),xmin,xmax)
    ax.grid(axis='x')
    return ax


def plot(algo_name: str, scheduled_data: Dict[str, List[Tuple[int, int]]]) -> None:
    # Dummy algorithm to directly plot scheduled data
    dummy_algo = Algorithm(algo_name, lambda x: x)
    
    ax = get_plot(dummy_algo, scheduled_data)
    
    ax.set_xlabel(algo_name)
    plt.show()