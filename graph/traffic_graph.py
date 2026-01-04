from langgraph.graph import StateGraph, END
from graph.state import TrafficState

from agents.input_agent import input_agent
from agents.metrics_agent import metrics_agent
from agents.insight_agent import insight_agent
from agents.output_agent import output_agent


def build_traffic_graph():
    # Initialize the state graph with the shared traffic state
    graph = StateGraph(TrafficState)

    # Register all processing agents as graph nodes
    graph.add_node("input", input_agent)
    graph.add_node("metrics", metrics_agent)
    graph.add_node("insight", insight_agent)
    graph.add_node("output", output_agent)

    # Define the starting point of the workflow
    graph.set_entry_point("input")

    # Establish the execution flow between agents
    graph.add_edge("input", "metrics")
    graph.add_edge("metrics", "insight")
    graph.add_edge("insight", "output")
    graph.add_edge("output", END)

    # Compile and return the executable graph
    return graph.compile()
