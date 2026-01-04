import pandas as pd

MONTHS = [
    "Jan", "Feb", "March", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
]

def metrics_agent(state):

    # Dictionary to store processed results for each table
    processed_tables = {}

    # Process each table loaded by the input agent
    for table_name, df in state["tables"].items():

        # Work on a copy to avoid mutating original data
        df = df.copy()

        # Keep only valid month rows and enforce correct month order
        df = df[df["Month"].isin(MONTHS)]
        df["Month"] = pd.Categorical(df["Month"], categories=MONTHS, ordered=True)
        df = df.sort_values("Month").reset_index(drop=True)

        # Ensure year columns are numeric for calculations
        for col in ["Year_2023", "Year_2024", "Year_2025"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Calculate Year-over-Year percentage change (2024 vs 2023)
        df["YOY % (2023-2024)"] = (
            (df["Year_2024"] - df["Year_2023"]) / df["Year_2023"] * 100
        ).round(2)

        # Calculate Month-over-Month percentage change for 2024
        df["LM% (2024)"] = (df["Year_2024"].diff() / df["Year_2024"].shift(1) * 100)

        # Handle January separately using December 2023 as the base month
        if "Dec" in df["Month"].values:
            dec_2023 = df.loc[df["Month"] == "Dec", "Year_2023"].values
            if len(dec_2023) > 0:
                jan_index = df.index[df["Month"] == "Jan"]
                if len(jan_index) > 0:
                    df.loc[jan_index, "LM% (2024)"] = (
                        (df.loc[jan_index, "Year_2024"] - dec_2023[0])
                        / dec_2023[0]
                        * 100
                    )

        df["LM% (2024)"] = df["LM% (2024)"].round(2)

        # Aggregate yearly totals for summary metrics
        total_2023 = df["Year_2023"].sum()
        total_2024 = df["Year_2024"].sum()
        total_2025 = df["Year_2025"].sum()

        # Calculate overall Year-over-Year change using annual totals
        percent_change_2024 = ((total_2024 - total_2023) / total_2023) * 100

        summary = {
            "total_2023": total_2023,
            "total_2024": total_2024,
            "total_2025": total_2025,
            "percent_change_2024": round(percent_change_2024, 2)
        }

        # Store monthly data and summary together for downstream agents
        processed_tables[table_name] = {
            "monthly_df": df,
            "summary": summary
        }

    # Attach all processed tables to shared state
    state["processed_tables"] = processed_tables
    return state
