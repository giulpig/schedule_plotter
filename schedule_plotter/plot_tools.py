# -*- coding: utf-8 -*-
"""
    plot_tools.py
    Functions to create and eventually show the plot
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from time import sleep
import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

import warnings
warnings.filterwarnings("error")

from schedule_plotter.Algorithm import Algorithm, Process
from typing import List, Tuple, Dict


class PlotUpdater:

    def __init__(self, algo: Algorithm, data: List[Process]):
        self._step = 0
        self.to_schedule = data
        self.algo = algo
        self.myplot = self.__call__(None)
        self.buttons = ()

    # Update method, called on button click
    def __call__(self, event):
        
        # Clear
        fig = plt.figure(num=1, clear=True)

        ax = fig.add_subplot(111)
        ax.set_xlabel(self.algo.name + str(self._step))

        
        # Run algorithm against Process list to create scheduled data
        scheduled_data = self.algo.function(self.to_schedule, interaction=True, step=self._step)

        yspan = len(scheduled_data)
        yplaces = [.5+i for i in range(yspan)]
        ylabels = sorted(scheduled_data.keys(), key=lambda name: int(name[1:]))

        ax.set_yticks(yplaces)
        ax.set_yticklabels(ylabels)


        try:
            xspan = max((j[1] for i in scheduled_data.values() for j in i))
        except:
            xspan = 0
            
        xplaces = [i for i in range(xspan)]
        xlabels = [str(i) for i in range(xspan)]

        ax.set_xticks(xplaces)    
        ax.set_xticklabels(xlabels)

        try:
            ax.set_ylim((0, yspan))
            low, hi = scheduled_data[ylabels[0]][0]
        except:
            ax.set_ylim((0, 1))
            low, hi = (0, 1)


        for pos, label in zip(yplaces, ylabels):
            for (start, end) in scheduled_data[label]:
                ax.add_patch(patches.Rectangle((start, pos-0.4/2.0), end-start, 0.4))
                if start < low:
                    low = start
                if end > hi:
                    hi = end

        # Draw an invisible line so that the x axis limits are automatically adjusted
        ax.plot((low, hi), (0, 0))

        xmin, xmax = ax.get_xlim()
        ax.hlines(range(1, yspan), int(xmin+0.5), int(xmax-0.5))
        ax.grid(axis='x')
        
        self.myplot = ax

        # Re-insert buttons
        axstep = plt.axes([0.9, 0.9, 0.11, 0.1])
        bstep = Button(axstep, 'Step', color='lightgreen', hovercolor='lightblue')
        bstep.on_clicked(self)
        
        axclose = plt.axes((0.0, 0.9, 0.1, 0.1))
        bclose = Button(axclose, 'Close', color='#f542e6', hovercolor='lightblue')
        bclose.on_clicked(PlotUpdater.closeplot)

        # Reference of buttons for garbage collector
        self.mybuttons = (bstep, bclose)

        plt.draw()
        self._step += 1

    # Method to close window
    @classmethod
    def closeplot(self, event):
        plt.close()


# algo must be of Algorithm type and data must be an array of Processes
def plot(algo: Algorithm, to_schedule: List[Process], interactive: bool = False) -> None:
    print(f"Plotting {algo.name} algorithm")

    if interactive:

        updater = PlotUpdater(algo, to_schedule)

        plt.show()
    
    else:
        # Get the plot object
        ax = get_plot(algo, to_schedule)

        plt.show()
        


def get_plot(algo: Algorithm, to_schedule: List[Process], delta:float = 0.4) -> matplotlib.figure.Figure:
    """:return: a drawing that you can manipulate, show, save etc"""

    # Clear
    fig = plt.figure(num=1, clear=True)

    ax = fig.add_subplot(111)
    ax.set_xlabel(algo.name)

    
    # Run algorithm against Process list to create scheduled data
    scheduled_data = algo.function(to_schedule)

    yspan = len(scheduled_data)
    yplaces = [.5+i for i in range(yspan)]
    ylabels = sorted(scheduled_data.keys(), key=lambda name: int(name[1:]))

    ax.set_yticks(yplaces)
    ax.set_yticklabels(ylabels)


    try:
        xspan = max((j[1] for i in scheduled_data.values() for j in i))
    except:
        xspan = 0

    ax.set_xticks([i for i in range(xspan)])    
    ax.set_xticklabels([str(i) for i in range(xspan)])

    try:
        ax.set_ylim((0, yspan))
        low, hi = scheduled_data[ylabels[0]][0]
    except:
        ax.set_ylim((0, 1))
        low, hi = (0, 1)


    for pos, label in zip(yplaces, ylabels):
        for (start, end) in scheduled_data[label]:
            ax.add_patch(patches.Rectangle((start, pos-delta/2.0), end-start, delta))
            if start < low:
                low = start
            if end > hi:
                hi = end

    # Draw an invisible line so that the x axis limits are automatically adjusted
    ax.plot((low, hi), (0, 0))

    xmin, xmax = ax.get_xlim()
    ax.hlines(range(1, yspan), int(xmin+0.5), int(xmax-0.5))
    ax.grid(axis='x')
    
    return ax



def plot_raw_data(algo_name: str, scheduled_data: Dict[str, List[Tuple[int, int]]]) -> None:
    # Dummy algorithm to directly plot scheduled data
    dummy_algo = Algorithm(algo_name, lambda x, interaction=False, step=-1: x)

    ax = get_plot(dummy_algo, scheduled_data)

    ax.set_xlabel(algo_name)
    plt.show()
