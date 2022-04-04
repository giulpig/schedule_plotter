# -*- coding: utf-8 -*-
"""
    FCFS.py
    Implementation of the FirstComeFirstServed scheduling algorithm
    using the schedule_plotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"


from typing import Dict, List, Tuple
from copy import deepcopy

from schedule_plotter.Algorithm import Algorithm
from schedule_plotter.Process import Process
from schedule_plotter.PriorityQueueWrapper import PriorityQueueWrapper

def run(processes: List[Process], interaction: bool = False) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0
    wait_time = 0

    processes_copy = deepcopy(processes)

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

        # Run it
        out[process.id] = [(time_now, time_now+process.duration)]

        time_now += process.duration

        wait_time += time_now-process.start-process.duration

    
    print(f"Average wait time is {wait_time/len(processes)}")

    return out
    

FCFS = Algorithm("FirstComeFirstServed", run)