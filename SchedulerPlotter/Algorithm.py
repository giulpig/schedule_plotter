"""
    Algorithm.py
    Class that describes a scheduling algorithm, see in detail how
    the run function should be implemented
"""

__author__ = "giulpig"
__license__ = "GPLv3"

from typing import Dict, List, Tuple
from SchedulerPlotter.Process import Process

class Algorithm:
    def __init__(self, name: str, function):
        self.name : str = name
        self.function = function

    # Dummy function for interface
    def function_interface(processes: List[Process]) -> Dict[str, List[Tuple[int, int]]]:
        """ 
        Interface for the scheduling algorithm function.
        
        :param processes: processes to schedule, in a list of Processes
        :return: dictionary with this layout:
            {
                "P1": [ (start0, end0), (start1, end1), ... ],
                "P2": [ (start0, end0), (start1, end1), ... ],
                ...
                "Pn": [ (start0, end0), (start1, end1), ... ]
            }
        """

        pass
