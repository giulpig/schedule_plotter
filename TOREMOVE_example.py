#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    main.py
    usage: 
        1- main.py (defaults to "input.csv" as input file)
        2- main.py {filename.csv}
    An executable script to test some scheduling algorithms
"""

__author__ = "giulpig"
__license__ = "GPLv3"

import sys

from schedule_plotter.Process import Process
from schedule_plotter.plot_tools import plot_raw_data, plot

from schedule_plotter.implementations.FCFS import FCFS
from schedule_plotter.implementations.SJF import SPN, SRT
from schedule_plotter.implementations.RoundRobin import RoundRobin


if __name__ == "__main__":

    # Generate data
    if len(sys.argv) == 1:
        try:
            dataset = Process.read_from_csv(sys.argv[1])
        except:
            dataset = Process.gen_n_random_in_range(9, (0,10), (1, 5), (-10,20))
    else:
        try:
            dataset = Process.read_from_csv(sys.argv[1])
        except:
            raise Exception("Invalid filename")

    # Plot FCFS using test funciton
    #plot(FCFS, dataset)
    print()

    # Direct plotting of SPN
    #print(f"Plotting {SPN.name} algorithm")
    #scheduled_data = SPN.function(dataset)
    #plot_raw_data(SPN.name, scheduled_data)
    print()

    # Plot SRT using test funciton
    #plot(SRT, dataset)
    print()

    # Plot RoundRobin
    plot(RoundRobin, dataset, interactive=True)
