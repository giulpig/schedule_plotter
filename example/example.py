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
from schedule_plotter.plot_tools import plot, test_schedule_algorithm

from schedule_plotter.implementations.FCFS import FCFS
from schedule_plotter.implementations.SJF import SJF
from schedule_plotter.implementations.RoundRobin import RoundRobin


if __name__ == "__main__":

    # Generate data
    if len(sys.argv) == 1:
        try:
            dataset = Process.read_from_csv(sys.argv[1])
        except:
            dataset = Process.gen_n_random_in_range(9, (0,1), (1, 3), (1,20))
    else:
        try:
            dataset = Process.read_from_csv(sys.argv[1])
        except:
            raise Exception("Invalid filename")

    # Plot FCFS using test funciton
    test_schedule_algorithm(FCFS, dataset)

    # Direct plotting of SJF
    print(f"Plotting {SJF.name} algorithm")
    scheduled_data = SJF.function(dataset)
    plot(SJF.name, scheduled_data)
            
    # Plot RoundRobin
    test_schedule_algorithm(RoundRobin, dataset)
