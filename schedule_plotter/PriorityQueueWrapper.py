# -*- coding: utf-8 -*-
"""
    PriorityQueueWrapper.py
    Wrapper class around PriorityQueue
"""

__author__ = "giulpig"
__license__ = "GPLv3"


#from queue import PriorityQueue
from collections import deque
from sortedcontainers import SortedDict

from numpy import sort

from schedule_plotter.Process import Process


class PriorityQueueWrapper:
    """
    Wrapper around PriorityQueue class to manage
    running queue
    """
    
    def __init__(self, sort_by: str = "FIFO"):
        """:param sortBy: can be 
            - "FIFO" (default)
            - "duration"
            - "priority"
            - "start"
            - "rem_time (remaining time)"
        """
        if sort_by == "FIFO":
            self.queue = deque()
        else:
            self.queue = SortedDict()

        self.sort_by = sort_by

    def __len__(self) -> int:
        return len(self.queue)

    def __str__(self) -> str:
        return str(self.queue)

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.queue):
            self.n += 1
            if self.sort_by == "FIFO":
                return self.queue[self.n-1]
            return (self.queue.peekitem(self.n-1))[1]
        else:
            raise StopIteration

    def put(self, proc: Process) -> None:
        if self.sort_by == "FIFO":
            self.queue.append(proc)
        elif self.sort_by == "duration":
            self.queue.update({proc.duration: proc})
        elif self.sort_by == "rem_time":
            self.queue.update({proc.remaining_time: proc})
        elif self.sort_by == "start":
            self.queue.update({proc.start: proc})
        elif self.sort_by == "priority":
            self.queue.update({proc.priority: proc})
        else:
            raise Exception("invalid sorting criterion")

    def pop(self) -> Process:
        if self.sort_by == "FIFO":
            return self.queue.popleft()

        (_, out) = self.queue.popitem(0)
        return out

    def set_sort_order(self, sort_by: str):
        if self.sort_by == sort_by:
            return
        
        if self.sort_by == "FIFO":
            temp = self.queue
        else:
            temp = self.queue.values()

        self.__init__(sort_by=sort_by)

        for i in temp:
            self.put(i)

        