# -*- coding: utf-8 -*-
"""
    RoundRobin.py
    Implementation of the RoundRobin scheduling algorithm
    using the schedule_plotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from copy import copy
from typing import Dict, List, Tuple

from schedule_plotter.Algorithm import Algorithm
from schedule_plotter.Process import Process
from schedule_plotter.PriorityQueueWrapper import PriorityQueueWrapper

# See interface in Algoritm class
def run(processes: List[Process], quantum: int = 1) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0
    wait_time = 0

    processes_copy = copy(processes)

    # FIFO queue
    ready_queue = PriorityQueueWrapper(sortBy="FIFO")

    while len(processes_copy)>0 or len(ready_queue)>0:
        
        # Insert new processes in queue
        while True:
            for proc in processes_copy[:]:
                if proc.start <= time_now:
                    ready_queue.put(proc)
                    processes_copy.remove(proc)

            if len(ready_queue) > 0:
                break
            
            time_now += 1

        # Get the process
        process = ready_queue.pop()

        duration = min(quantum, process.duration)

        # Run it
        if process.id in out.keys():
            out[process.id].append((time_now, time_now+duration))
        else:
            out[process.id] = [(time_now, time_now+duration)]

        # Re-insert it if it is not finished
        process.duration -= duration
        if process.duration > 0:
            process.start = time_now + duration
            processes_copy.append(process)
        else:
            wait_time += time_now-process.start

        time_now += duration

    print(f"Average wait time is {wait_time/len(processes)}")

    return out
    

RoundRobin = Algorithm("RoundRobin", run)