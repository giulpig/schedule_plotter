"""
    RoundRobin.py
    Implementation of the RoundRobin scheduling algorithm
    using the SchedulerPlotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from copy import copy
from typing import Dict, List, Tuple

from SchedulerPlotter.Algorithm import Algorithm
from SchedulerPlotter.Process import Process

# See interface in Algoritm class
def run(processes: List[Process], quantum: int = 1) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0

    processes_copy = copy(processes)

    # FIFO queue
    running_queue = PriorityQueueWrapper()

    # Insert initial processes in queue
    for proc in processes:
        if proc.start == 0:
            running_queue.put(proc)
            processes_copy.remove(proc)

    while len(processes_copy)>0 or len(running_queue)>0:
        
        if len(running_queue) == 0:
            time_now += 1
            continue

        # Get the process
        process = running_queue.get()

        # Run it
        out[process.id] = [(time_now, time_now+process.duration)]

        # Insert new processes in queue
        for _ in range(time_now+1, time_now+process.duration+1):
            for proc in processes_copy[:]:
                if proc.start <= time_now:
                    running_queue.put(proc)
                    processes_copy.remove(proc)

        time_now += process.duration

    return out
    

RoundRobin = Algorithm("RoundRobin", run)