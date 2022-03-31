"""
    FCFS.py
    Implementation of the FirstComeFirstServed scheduling algorithm
    using the SchedulerPlotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"


from typing import Dict, List, Tuple
from copy import copy

from SchedulerPlotter.Algorithm import Algorithm
from SchedulerPlotter.Process import Process
from SchedulerPlotter.PriorityQueueWrapper import PriorityQueueWrapper

def run(processes: List[Process]) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0

    processes_copy = copy(processes)

    # FIFO queue
    running_queue = PriorityQueueWrapper(sortBy="FIFO")


    while len(processes_copy)>0 or len(running_queue)>0:
        
        # Insert new processes in queue
        while True:
            for proc in processes_copy[:]:
                if proc.start <= time_now:
                    running_queue.put(proc)
                    processes_copy.remove(proc)

            if len(running_queue) > 0:
                break
            
            time_now += 1

        # Get the process
        process = running_queue.pop()

        # Run it
        out[process.id] = [(time_now, time_now+process.duration)]

        time_now += process.duration

    return out
    

FCFS = Algorithm("FirstComeFirstServed", run)