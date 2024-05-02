from typing_extensions import TypedDict
from typing import List


class AgentState(TypedDict):
    # The customer name to search for in the Todoist API
    customer_name: str
    # The descriptions of the tasks that have been completed
    task_descriptions: List[str]
    # The combined description of each task description created by the llm
    registration_description: str
