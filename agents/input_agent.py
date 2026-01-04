import pandas as pd

INPUT_PATH = "data/input/traffic_input.xlsx"

REQUIRED_COLUMNS = [
    "Month",
    "Year_2023",
    "Year_2024",
    "Year_2025"
]

def input_agent(state):
    # Load the Excel file that contains all traffic-related tables
    xls = pd.ExcelFile(INPUT_PATH)

    # Dictionary to store each sheet as a separate dataframe
    tables = {}

    # Loop through all sheets present in the input Excel file
    for sheet in xls.sheet_names:
        # Read the current sheet into a dataframe
        df = pd.read_excel(xls, sheet)

        # Check whether all required columns exist in the sheet
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(
                f"Sheet '{sheet}' is missing columns: {missing}"
            )

        # Convert yearly traffic columns to numeric values for calculations
        for col in ["Year_2023", "Year_2024", "Year_2025"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Store the validated dataframe using the sheet name as key
        tables[sheet] = df

    # Save all loaded tables into the shared state for downstream agents
    state["tables"] = tables

    # Add a log entry to track successful data loading
    state.setdefault("logs", []).append(
        "Input Agent: Data loaded and validated successfully"
    )

    return state
