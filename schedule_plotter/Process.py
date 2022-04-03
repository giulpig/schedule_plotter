# -*- coding: utf-8 -*-
"""
    Processes.py
    Process class, provides some basic properties and functions
"""

__author__ = "giulpig"
__license__ = "GPLv3"


import random
import csv
from typing import Any, Tuple, List

class Process:
    def __init__(self, id: int, start: int, duration: int, priority: int):
        self.id : str = f"P{id}"
        self.start: int = start
        self.duration : int = duration
        self.priority : int = priority
        self.remaining_time: int = duration

    def __gt__(self, other):
        return self.id > other.id

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self) -> str:
        return f"id: {self.id}, remaining time: {self.remaining_time}"
    
    def __repr__(self) -> str:
        return f"id: {self.id}, remaing time: {self.remaining_time}"


    @classmethod
    def gen_n_random_in_range(cls, n:int, start_range: Tuple[int,int], dur_range: Tuple[int,int], prio_range: Tuple[int,int]) -> List[Any]:
        
        out = []

        for i in range(n):
            out.append(Process(i, random.randint(start_range[0], start_range[1]), random.randint(dur_range[0], dur_range[1]), random.randint(prio_range[0], prio_range[1])))

        return out


    @classmethod
    def read_from_csv(cls, filename: str) -> List[Any]:
        
        out = []

        with open(filename, "r") as in_file:
            csv_reader = csv.reader(in_file, delimiter=',')
            for row in csv_reader:
                if csv_reader.line_num == 1:
                    # Skip column name
                    pass
                else:
                    out.append(Process(int(row[0]), int(row[1]), int(row[2]), int(row[3])))

        return out