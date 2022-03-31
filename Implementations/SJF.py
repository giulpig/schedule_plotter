"""
    SJF.py
    Implementation of the ShortestJobFirst scheduling algorithm
    using the SchedulerPlotter packcage
"""

__author__ = "giulpig"
__license__ = "GPLv3"


import queue
from typing import Dict, List, Tuple
from queue import PriorityQueue
from copy import copy

from SchedulerPlotter.Algorithm import Algorithm
from SchedulerPlotter.Process import Process

# Priority queue wrapper that sorts by duration
class PriorityQueueWrapper:
    
    def __init__(self):
        self.queue = PriorityQueue()

    def __len__(self):
        return self.queue._qsize()

    def __str__(self):
        temp = []
        while self.queue.qsize() > 0:
            temp.append(self.queue.get())
        for i in temp:
            self.queue.put(i)

        return str([i[1] for i in temp])

    def put(self, proc: Process) -> None:
        self.queue.put((proc.duration, proc))

    def get(self) -> Process:
        (_, out) = self.queue.get()
        return out


def run(processes: List[Process]) -> Dict[str, List[Tuple[int, int]]]:
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

    print(running_queue)

    while len(processes_copy)>0 or len(running_queue)>0:
        
        if len(running_queue) == 0:
            time_now += 1
            continue

        # Get the process
        process = running_queue.get()

        # Run it
        out[process.id] = [(time_now, time_now+process.duration)]

        # Insert new processes in queue
        for i in range(time_now+1, time_now+process.duration+1):
            for proc in processes:
                if proc.start <= time_now:
                    running_queue.put(proc)
                    if proc in processes_copy:
                        processes_copy.remove(proc)

        time_now += process.duration

    return out
    

SJF = Algorithm("ShortestJobFirst", run)