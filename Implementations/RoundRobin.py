"""
    RoundRobin.py
    Implementation of the RoundRobin scheduling algorithm
    using the SchedulerPlotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from copy import copy
from typing import Dict, List, Tuple

from numpy import empty
from SchedulerPlotter.Algorithm import Algorithm
from SchedulerPlotter.Process import Process

# See interface in Algoritm class
def run(processes: List[Process], quantum: int = 1) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0
    index_now = 0

    dataset_copy = copy(processes)
    while len(dataset_copy)>0:
        
        index_now %= len(dataset_copy)
        process = dataset_copy[index_now]

        if(process.duration == 0):
            dataset_copy.remove(process)
            continue

        process_time = min(process.duration, quantum)

        if len(dataset_copy) == 1:
            process_time = process.duration

        if process.id in out:
            out[process.id].append((time_now, time_now+process_time))
        else:
            out[process.id] = [(time_now, time_now+process_time)]

        process.duration -= process_time

        index_now = (index_now+1) % len(dataset_copy)

        time_now += process_time
        

    return out
    

RoundRobin = Algorithm("RoundRobin", run)