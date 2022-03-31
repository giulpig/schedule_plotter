"""
    PriorityQueueWrapper.py
    Wrapper class around PriorityQueue
"""

__author__ = "giulpig"
__license__ = "GPLv3"


from queue import PriorityQueue

from Process import Process


class PriorityQueueWrapper:
    """
    Wrapper around PriorityQueue class to manage
    running queue
    """
    
    def __init__(self, sortBy: str = "duration"):
        """:param sortBy: can be 
            - "duration" (default)
            - "priority"
            - "start"
            - "id"
        """
        self.queue = PriorityQueue()
        self.sortBy = sortBy

    def __len__(self) -> int:
        return self.queue._qsize()

    def __str__(self) -> str:
        temp = []
        while self.queue.qsize() > 0:
            temp.append(self.queue.get())
        for i in temp:
            self.queue.put(i)

        return str([i[1] for i in temp])

    def put(self, proc: Process) -> None:
        if self.sortBy == "duration":
            self.queue.put((proc.duration, proc))
        elif self.sortBy == "id":
            self.queue.put((proc.id, proc))
        elif self.sortBy == "start":
            self.queue.put((proc.start, proc))
        elif self.sortBy == "priority":
            self.queue.put((proc.priority, proc))
        else:
            raise Exception("invalid sorting criterion")

    def get(self) -> Process:
        (_, out) = self.queue.get()
        return out