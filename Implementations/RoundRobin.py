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
from SchedulerPlotter.PriorityQueueWrapper import PriorityQueueWrapper

# See interface in Algoritm class
def run(processes: List[Process], quantum: int = 1) -> Dict[str, List[Tuple[int, int]]]:
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

        duration = min(quantum, process.duration)

        # Run it
        if process.id in out.keys():
            out[process.id].append((time_now, time_now+duration))
        else:
            out[process.id] = [(time_now, time_now+duration)]

        # Re-insert it if it is not finished
        process.duration -= duration
        process.start = time_now + duration
        if process.duration > 0:
            processes_copy.append(process)

        time_now += duration

    return out
    

RoundRobin = Algorithm("RoundRobin", run)