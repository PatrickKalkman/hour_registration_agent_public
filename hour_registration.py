from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agent_state import AgentState
from nodes.customer_name_node import customer_name_node
from nodes.task_fetcher_node import task_fetcher_node
from nodes.data_entry_node import data_entry_node
from nodes.time_registration_description_node import time_registration_description_node

load_dotenv()

workflow = StateGraph(AgentState)
workflow.add_node("customer_name_node", customer_name_node)
workflow.add_node("task_fetcher_node", task_fetcher_node)
workflow.add_node("time_registration_description_node_llm", time_registration_description_node)
workflow.add_node("data_entry_node", data_entry_node)

workflow.set_entry_point("customer_name_node")
workflow.add_edge("customer_name_node", "task_fetcher_node")
workflow.add_edge("task_fetcher_node", "time_registration_description_node_llm")
workflow.add_edge("time_registration_description_node_llm", "data_entry_node")
workflow.add_edge("data_entry_node", END)
app = workflow.compile()

for s in app.stream({}):
    print(list(s.values())[0])
