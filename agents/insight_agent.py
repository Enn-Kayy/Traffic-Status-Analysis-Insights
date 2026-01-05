import pandas as pd
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.2
)

def insight_agent(state):

    insights = {}

    for name, data in state["processed_tables"].items():
        df = data["monthly_df"]

        total_2023 = df["Year_2023"].sum()
        total_2024 = df["Year_2024"].sum()

        yoy_total = ((total_2024 - total_2023) / total_2023) * 100

        trend_direction = (
            "growth" if yoy_total > 0
            else "decline" if yoy_total < 0
            else "stable performance"
        )

        prompt = f"""
You are a senior business analytics consultant preparing insights for company management.

Context:
- Table name: {name}
- Total traffic 2023: {round(total_2023, 2)}
- Total traffic 2024: {round(total_2024, 2)}
- Year-over-Year change: {round(yoy_total, 2)}%
- Overall trend direction: {trend_direction}

Task:
Write a clear, professional, management-level insight that:
1. Summarizes overall yearly performance (not month-wise noise)
2. Explains what the YoY trend indicates for business growth or decline
3. Provides strategic interpretation, not technical explanation
4. Avoids recommendations or next steps
5. Sounds suitable for leadership reporting

Output format:
- Use headings
- Use complete sentences
- Keep tone formal and concise
"""

        response = llm.invoke(prompt)

        insights[name] = response.content.strip()

    state["insights"] = insights
    return state

