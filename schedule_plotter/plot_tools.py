# -*- coding: utf-8 -*-
"""
    plot_tools.py
    Functions to create and eventually show the plot
"""

__author__ = "giulpig"
__license__ = "GPLv3"

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button

from typing import List

# TOREMOVE, just for debugging
import warnings
warnings.filterwarnings("error")

import sys

from schedule_plotter.Algorithm import Algorithm, Process
from schedule_plotter.PriorityQueueWrapper import PriorityQueueWrapper


class PlotUpdater:

    def __init__(self, algo: Algorithm, data: List[Process], interactive, context_switch_time, quantum):
        self.intercative = interactive
        if interactive:
            self._step = 0
        else:
            self._step = -1

        self.switch_time = context_switch_time
        self.quantum = quantum
        self.to_schedule = data
        self.algo = algo
        self.buttons = ()
        self.ready_queue = PriorityQueueWrapper()
        self.myplot = self.__call__(None)

    # Update method, called on button click
    def __call__(self, event):
        
        # Clear
        fig = plt.figure(num=1, clear=True, figsize=(10, 8))

        ax = fig.add_subplot(111)
        
        if self._step == -1:
            ax.set_xlabel(self.algo.name)
        else:
            ax.set_xlabel(self.algo.name + " - " + str(self._step))

        # Create an empty ready queue to feed to the algorithm
        self.ready_queue = PriorityQueueWrapper()
        
        # Run algorithm against Process list to create scheduled data
        if self.algo.name == "RoundRobin":
            scheduled_data = self.algo.function(self.to_schedule, step=self._step, ready_queue=self.ready_queue, switch_time=self.switch_time, quantum=self.quantum)
        else:
            scheduled_data = self.algo.function(self.to_schedule, step=self._step, ready_queue=self.ready_queue, switch_time=self.switch_time)
        
        yspan = len(scheduled_data)
        yplaces = [.5+i for i in range(yspan)]
        ylabels = sorted(scheduled_data.keys(), key=lambda name: int(name[1:]))

        ax.set_yticks(yplaces)
        ax.set_yticklabels(ylabels)


        try:
            xspan = max((j[1] for i in scheduled_data.values() for j in i[1]))
        except:
            xspan = 0
            
        xplaces = [i for i in range(int(xspan+0.5))]
        xlabels = [str(i) for i in range(int(xspan+0.5))]

        ax.set_xticks(xplaces)    
        ax.set_xticklabels(xlabels)

        try:
            ax.set_ylim((0, yspan))
            low, high = scheduled_data[ylabels[0]][0][0]
        except:
            ax.set_ylim((0, 1))
            low, high = (0, 1)


        for pos, label in zip(yplaces, ylabels):
            # Plot executing and in_queue processes
            in_queue, executing = scheduled_data[label]
            for (start, end) in in_queue:
                
                if start == end:
                    continue

                ax.add_patch(patches.Rectangle((start, pos-0.4/2.0), end-start, 0.4, color="#ccff99"))

                low = min(start, low)
                high = max(end, high)

            for (start, end) in executing:
                
                if start == end:
                    continue
                
                ax.add_patch(patches.Rectangle((start, pos-0.4/2.0), end-start, 0.4, color="#3366ff"))

                low = min(start, low)
                high = max(end, high)

        # Draw an invisible line so that the x axis limits are automatically adjusted
        ax.plot((low, high), (0, 0))

        xmin, xmax = ax.get_xlim()
        ax.hlines(range(1, yspan), int(xmin+0.5), int(xmax-0.5))
        ax.grid(axis='x')
        
        self.myplot = ax

        # Insert buttons
        if self.buttons == ():
            temp_axes = plt.axes([0.9, 0.9, 0.1, 0.1])
            bclose = Button(temp_axes, 'Close', color='red', hovercolor='lightblue')
            bclose.on_clicked(PlotUpdater.exitall)

            temp_axes = plt.axes((0.75, 0.9, 0.15, 0.1))
            bnext = Button(temp_axes, 'Next plot', color='#f0a8e4', hovercolor='lightblue')
            bnext.on_clicked(PlotUpdater.closeplot)

            if self.intercative:
                temp_axes = plt.axes((0.0, 0.9, 0.12, 0.1))
                bstep = Button(temp_axes, 'Step', color='lightgreen', hovercolor='lightblue')
                bstep.on_clicked(self)
            
                temp_axes = plt.axes((0.12, 0.9, 0.15, 0.1))
                bprint = Button(temp_axes, 'Print Queue', color='yellow', hovercolor='lightblue')
                bprint.on_clicked(self.print_queue)

                temp_axes = plt.axes((0.27, 0.9, 0.15, 0.1))
                bend = Button(temp_axes, 'Go to end', color='#6699ff', hovercolor='lightblue')
                bend.on_clicked(self.goto_end)
            
            else:
                bstep = None
                bprint = None
                bend = None

            # Reference buttons for garbage collector
            self.mybuttons = (bstep, bnext, bclose, bprint, bend)

        plt.draw()
        self._step += 1

    # Method to go to next plot
    @classmethod
    def closeplot(_self, event) -> None:
        plt.close()

    # Method to stop execution
    @classmethod
    def exitall(_self, event) -> None:
        plt.close()
        sys.exit()

    def print_queue(self, event) -> None:
        print("Printing ready queue")
        for i in self.ready_queue:
            print(f"\t{i.id} - remaning time: {i.remaining_time}")
        print()

    def goto_end(self, event):
        self._step = -1
        self.__call__(None)

            

# algo must be of Algorithm type and data must be an array of Processes
def plot(algo: Algorithm, to_schedule: List[Process], interactive: bool = False, context_switch_time: float = 0, quantum: int = 0) -> None:
    print(f"Plotting {algo.name} algorithm\n")

    updater = PlotUpdater(algo, to_schedule, interactive, context_switch_time, quantum)

    plt.show()
