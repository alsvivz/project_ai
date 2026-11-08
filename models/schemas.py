from pydantic import BaseModel
from typing import List

class TaskRequirements(BaseModel):
    language: str
    task_goal: str
    input_data: List[str]
    output_data: List[str]
    constraints: List[str]
    concepts: List[str]
    edge_cases: List[str]
    acceptance_criteria: List[str]
    ambiguities: List[str]
    assumptions: List[str]