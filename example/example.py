#!/usr/bin/env python

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

from schedule_plotter import Process, plot, test_schedule_algorithm

from Implementations.FCFS import FCFS
from Implementations.SJF import SJF
from Implementations.RoundRobin import RoundRobin


if __name__ == "__main__":

    # Read data from csv
    if len(sys.argv) == 1:
        dataset = Process.read_from_csv("input.csv")
    else:
        try:
            dataset = Process.read_from_csv(sys.argv[1])
        except:
            raise Exception("Invalid filename")

    # Generate random processes. As for ranges, last element is not included
    #dataset = Process.gen_n_random_in_range(9, (0,1), (1, 3), (1,20))

    # Plot FCFS using test funciton
    test_schedule_algorithm(FCFS, dataset)

    # Direct plotting of SJF
    scheduled_data = SJF.function(dataset)
    print(f"Plotting {SJF.name} algorithm")
    plot(SJF.name, scheduled_data)
            
    # Plot RoundRobin
    test_schedule_algorithm(RoundRobin, dataset)
