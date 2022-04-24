# -*- coding: utf-8 -*-
"""
    Algorithm.py
    Class that describes a scheduling algorithm, see in detail how
    the run function should be implemented
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from typing import Dict, List, Tuple
from schedule_plotter.Process import Process
from schedule_plotter.PriorityQueueWrapper import PriorityQueueWrapper

class Algorithm:
    def __init__(self, name: str, function):
        self.name : str = name
        self.function = function

    # Dummy function for pseudo-interface for "function" argument
    def run(processes: List[Process], ready_queue: PriorityQueueWrapper, interaction: bool = False, step: int = -1, switch_time: float = 0) -> Dict[str, Tuple[ List[Tuple[int, int]], List[Tuple[int, int]] ]]:
        """ 
        Interface for the scheduling algorithm function.
        
        :param processes: processes to schedule, in a list of Processes
        :return: dictionary with this layout:
            {
                "P0": ([(start_queue0, end_queue0), ...], [ (start_exec0, end_exec0), ... ]),
                "P1": ([(start_queue0, end_queue0), ...], [ (start_exec0, end_exec0), ... ]),
                ...
                "Pn-1": ([(start_queue0, end_queue0), ...], [ (start_exec0, end_exec0), ... ])
            }
        """
        ...
