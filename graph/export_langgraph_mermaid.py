import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from traffic_graph import build_traffic_graph


def export_mermaid_from_langgraph():
    app = build_traffic_graph()

    mermaid_code = app.get_graph().draw_mermaid()

    os.makedirs("docs", exist_ok=True)
    path = "docs/langgraph_orchestration.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write("# 🧠 LangGraph Orchestration Diagram\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_code)
        f.write("\n```")

    print(f"✅ LangGraph Mermaid diagram saved at: {path}")


if __name__ == "__main__":
    export_mermaid_from_langgraph()
