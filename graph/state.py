from typing import TypedDict, Dict, Any
import pandas as pd

class TrafficState(TypedDict):
    # input
    input_path: str

    # raw tables from Excel
    tables: Dict[str, pd.DataFrame]

    # processed tables (after metrics)
    processed_tables: Dict[str, Dict[str, Any]]

    # insights text
    insights: Dict[str, str]
