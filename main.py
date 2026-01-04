from graph.traffic_graph import build_traffic_graph

def main():
    # Build the traffic analysis workflow using LangGraph
    app = build_traffic_graph()

    # Initialize the shared state passed across all agents
    initial_state = {
        "input_path": "data/input/traffic_input.xlsx",
        "tables": {},
        "processed_tables": {},
        "insights": {},
        "logs": []
    }

    # Execute the complete traffic status pipeline
    app.invoke(initial_state)
    print("✅ Traffic Status pipeline executed successfully")

if __name__ == "__main__":
    # Entry point for running the pipeline
    main()
