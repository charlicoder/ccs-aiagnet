from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from chatbots.utils.state import AgentState
from chatbots.utils.nodes import *
from chatbots.utils.tools import *

from dotenv import load_dotenv
import os

load_dotenv()

# Define a new graph
workflow = StateGraph(AgentState)


workflow.add_node("chatbot", chatbot)
# workflow.add_node("tools", tool_node)

workflow.add_conditional_edges(
    "chatbot",
    tools_condition,
)
workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

# Compile
# graph = workflow.compile()

graph_builder = StateGraph(MessagesState)
graph_builder.add_node(query_or_respond)
graph_builder.add_node(tool_nodes)
graph_builder.add_node(generate)

graph_builder.set_entry_point("query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)

graph = graph_builder.compile()
