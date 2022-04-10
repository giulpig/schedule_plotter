# -*- coding: utf-8 -*-
"""
    SJF.py
    Implementation of the ShortestProcessNext and ShortestRemainingTime
    scheduling algorithms using the schedule_plotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from typing import Dict, List, Tuple
from copy import deepcopy

from schedule_plotter.Algorithm import Algorithm
from schedule_plotter.Process import Process
from schedule_plotter.PriorityQueueWrapper import PriorityQueueWrapper
from schedule_plotter import config



def spn_run(processes: List[Process], ready_queue: PriorityQueueWrapper, interaction: bool = False, step: int = -1) -> Dict[str, Tuple[ List[Tuple[int, int]], List[Tuple[int, int]] ]]:
    out = {}
    time_now = 0
    wait_time = 0

    processes_copy = deepcopy(processes)

    ready_queue.set_sort_order("duration")

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

        # Run it by storing process lifetime (in queue and executing)
        if process.id in out.keys():
            out[process.id][0].append((process.start, time_now))
            out[process.id][1].append((time_now, time_now+process.duration))
        else:
            out[process.id] = [(process.start, time_now)], [(time_now, time_now+process.duration)]


        wait_time += time_now-process.start

        time_now += process.duration

        step -= 1

    if config.print_stats:
        print(f"Average wait time is {wait_time/len(processes)}")

    return out

SPN = Algorithm("ShortestProcessNext", spn_run)



def srt_run(processes: List[Process], ready_queue: PriorityQueueWrapper, interaction: bool = False, step: int = -1) -> Dict[str, Tuple[ List[Tuple[int, int]], List[Tuple[int, int]] ]]:
    out = {}
    time_now = 0
    wait_time = 0
    
    processes_copy = deepcopy(processes)

    ready_queue.set_sort_order("rem_time")

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

        # Run it by storing process lifetime (in queue and executing)
        if process.id in out.keys():
            out[process.id][0].append((process.start, time_now))
            out[process.id][1].append((time_now, time_now+1))
        else:
            out[process.id] = [(process.start, time_now)], [(time_now, time_now+1)]


        process.remaining_time -= 1

        time_now += 1

        # Re-insert it if it is not finished
        if process.remaining_time > 0:
            ready_queue.put(process)
        else:
            wait_time += time_now-process.start-process.duration

        step -= 1

    if config.print_stats:
        print(f"Average wait time is {wait_time/len(processes)}")

    return out


SRT = Algorithm("ShortestRemainingTime", srt_run)
