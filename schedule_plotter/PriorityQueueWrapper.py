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
            if not proc.duration in self.queue:
                self.queue.update({proc.duration: [proc]})
            else:
                self.queue[proc.duration].append(proc)

        elif self.sort_by == "rem_time":
            if not proc.remaining_time in self.queue:
                self.queue.update({proc.remaining_time: [proc]})
            else:
                self.queue[proc.remaining_time].append(proc)

        elif self.sort_by == "start":
            if not proc.start in self.queue:
                self.queue.update({proc.start: [proc]})
            else:
                self.queue[proc.start].append(proc)

        elif self.sort_by == "priority":
            if not proc.priority in self.queue:
                self.queue.update({proc.priority: [proc]})
            else:
                self.queue[proc.priority].append(proc)

        else:
            raise Exception("invalid sorting criterion")

    def pop(self) -> Process:
        if self.sort_by == "FIFO":
            return self.queue.popleft()

        if len(self.queue.peekitem(0)[1]) == 1:
            out = self.queue.popitem(0)[1][0]
        else:
            out = self.queue.peekitem(0)[1].pop()

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
            for j in temp:
                self.put(j)

        