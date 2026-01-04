import pandas as pd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables such as API keys
load_dotenv()

# Initialize Groq LLM for future extensibility
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

def insight_agent(state):

    # Dictionary to store generated insights for each table
    insights = {}

    # Iterate through all processed tables
    for name, data in state["processed_tables"].items():
        df = data["monthly_df"]

        # Extract the latest available month for reference
        latest = df.iloc[-1]

        # Calculate total traffic for yearly comparison
        total_2023 = df["Year_2023"].sum()
        total_2024 = df["Year_2024"].sum()

        # Compute overall Year-over-Year growth percentage
        yoy_total = ((total_2024 - total_2023) / total_2023) * 100

        # Determine the overall performance direction
        trend_direction = (
            "growth" if yoy_total > 0
            else "decline" if yoy_total < 0
            else "stable performance"
        )

        # Generate a management-level insight summary
        insight = f"""
### Overall Performance Insight

The overall traffic performance shows a **{trend_direction} trend in 2024 compared to 2023**, with a **Year-over-Year change of {round(yoy_total, 2)}%**.

This indicates that the platform has {"successfully expanded its reach and engagement" if yoy_total > 0 else "experienced a contraction in overall traffic levels"} over the year. The data suggests that performance shifts are not isolated to a single month but reflect a **broader annual movement**.

Month-over-Month variations observed throughout the year represent short-term fluctuations; however, the **primary business signal remains the overall yearly direction**, which should be the key focus for strategic decision-making.

### Management Perspective
- The current trend highlights the effectiveness of existing traffic acquisition and engagement strategies at an annual level.
- Sustaining and improving this trajectory will require reinforcing high-performing channels and addressing areas contributing to weaker periods.
- Continued monitoring of overall growth patterns is recommended to ensure long-term stability and scalability.

*This insight summarizes overall traffic movement and is intended to support strategic planning and performance evaluation.*
        """.strip()

        # Store the generated insight for the current table
        insights[name] = insight

    # Attach all insights to the shared state for downstream usage
    state["insights"] = insights
    return state
