# -*- coding: utf-8 -*-
"""
    PriorityQueueWrapper.py
    Wrapper class around PriorityQueue
"""

__author__ = "giulpig"
__license__ = "GPLv3"


from queue import PriorityQueue
from collections import deque

from schedule_plotter.Process import Process


class PriorityQueueWrapper:
    """
    Wrapper around PriorityQueue class to manage
    running queue
    """
    
    def __init__(self, sortBy: str = "FIFO"):
        """:param sortBy: can be 
            - "FIFO" (default)
            - "duration"
            - "priority"
            - "start"
            - "rem_time (remaining time)"
        """
        if sortBy == "FIFO":
            self.queue = deque()
        else:
            self.queue = PriorityQueue()

        self.sortBy = sortBy

    def __len__(self) -> int:
        if self.sortBy == "FIFO":
            return len(self.queue)
        else:
            return self.queue._qsize()

    def __str__(self) -> str:

        if self.sortBy == "FIFO":
            return str(self.queue)

        temp = []
        while self.queue.qsize() > 0:
            temp.append(self.queue.get())
        for i in temp:
            self.queue.put(i)

        return f"PriorityQueue{[i[1] for i in temp]}"

    def put(self, proc: Process) -> None:
        if self.sortBy == "FIFO":
            self.queue.append(proc)
        elif self.sortBy == "duration":
            self.queue.put((proc.duration, proc))
        elif self.sortBy == "rem_time":
            self.queue.put((proc.remaining_time, proc))
        elif self.sortBy == "start":
            self.queue.put((proc.start, proc))
        elif self.sortBy == "priority":
            self.queue.put((proc.priority, proc))
        else:
            raise Exception("invalid sorting criterion")

    def pop(self) -> Process:

        if self.sortBy == "FIFO":
            return self.queue.popleft()

        (_, out) = self.queue.get()
        return out