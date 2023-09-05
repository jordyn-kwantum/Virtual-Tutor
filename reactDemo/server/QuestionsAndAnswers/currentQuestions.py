from dataclasses import dataclass, field
from typing import List

"""
This is a simple dataclass that stores the list of Ids of the currently considered questions.
Thic class is used a lot else in the code.
"""

@dataclass
class localQuestion:
    id:int
    questions:List[str] = field(default_factory=list) 
    AzureQuestion:List[str] = field(default_factory=list) 


    answer:str = ""
    source:str = ""
    context:str = ""
    rating:int = 0

    inAzure:int = 0
    AzureId:int = -1
    AzureAnswer:str = ""
    AzureRating:int = -1

    team2question:str = ""

    selected:bool = False
    


