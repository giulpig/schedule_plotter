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



def spn_run(processes: List[Process], interactive: bool = False) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0
    wait_time = 0

    processes_copy = deepcopy(processes)

    ready_queue = PriorityQueueWrapper(sortBy="duration")

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

        wait_time += time_now-process.start

        time_now += process.duration

    print(f"Average wait time is {wait_time/len(processes)}")

    return out

SPN = Algorithm("ShortestProcessNext", spn_run)



def srt_run(processes: List[Process], interactive: bool = False) -> Dict[str, List[Tuple[int, int]]]:
    out = {}
    time_now = 0
    wait_time = 0

    processes_copy = deepcopy(processes)

    ready_queue = PriorityQueueWrapper(sortBy="rem_time")

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

        # Run it for 1 unit of time
        if process.id in out.keys():
            out[process.id].append((time_now, time_now+1))
        else:
            out[process.id] = [(time_now, time_now+1)]

        process.remaining_time -= 1

        time_now += 1

        # Re-insert it if it is not finished
        if process.remaining_time > 0:
            processes_copy.append(process)
        else:
            wait_time += time_now-process.start-process.duration


    print(f"Average wait time is {wait_time/len(processes)}")

    return out


SRT = Algorithm("ShortestRemainingTime", srt_run)
