# -*- coding: utf-8 -*-
"""
    RoundRobin.py
    Implementation of the RoundRobin scheduling algorithm
    using the schedule_plotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from copy import deepcopy
from typing import Dict, List, Tuple

from schedule_plotter.Algorithm import Algorithm
from schedule_plotter.Process import Process
from schedule_plotter.PriorityQueueWrapper import PriorityQueueWrapper
from schedule_plotter import config

# See interface in Algoritm class
def run(processes: List[Process], ready_queue: PriorityQueueWrapper, step: int = -1, quantum: int = 1) -> Dict[str, Tuple[ List[Tuple[int, int]], List[Tuple[int, int]] ]]:
    out = {}
    time_now = 0
    wait_time = 0

    processes_copy = deepcopy(processes)

    # FIFO queue
    ready_queue.set_sort_order("FIFO")

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

        if step == 0:
            break

        # Get the process
        process = ready_queue.pop()

        burst_time = min(quantum, process.remaining_time)

        # Run and store process burst time
        if process.id in out:
            out[process.id][1].append((time_now, time_now+burst_time))
        else:
            out[process.id] = [], [(time_now, time_now+burst_time)]


        time_now += burst_time

        # Re-insert it if it is not finished
        process.remaining_time -= burst_time
        if process.remaining_time > 0:
            processes_copy.append(process)
        else:

            if process.id in out:
                out[process.id][0].append((process.start, time_now-burst_time))
            else:
                out[process.id] = [(process.start, time_now-burst_time)], []

            wait_time += time_now-process.start-process.duration

        step -= 1

    # Add in_queue slices
    for seq in (processes_copy, ready_queue):
        for proc in seq:
            if proc.start < time_now:
                if proc.id in out:
                    out[proc.id][0].append((proc.start, time_now))
                else:
                    out[proc.id] = [(proc.start, time_now)], []
    
    if config.print_stats:
        print(f"Average wait time is {wait_time/len(processes)}")

    return out
    

RoundRobin = Algorithm("RoundRobin", run)