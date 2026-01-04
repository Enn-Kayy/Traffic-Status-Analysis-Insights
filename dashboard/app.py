import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

MONTH_ORDER = [
    "Jan", "Feb", "March", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Load the generated Excel report
xls = pd.ExcelFile("data/output/traffic_report.xlsx")

st.title("Traffic Status Dashboard")

# Allow user to select a specific traffic table
table = st.selectbox("Select Table", xls.sheet_names)

# Read raw sheet data to extract summary values
raw = pd.read_excel(xls, table, header=None)

def get_value(label):
    row = raw[raw[0] == label]
    return row.iloc[0, 1] if not row.empty else "N/A"

# Display high-level KPI metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total 2023", get_value("Total 2023"))
col2.metric("Total 2024", get_value("Total 2024"))
col3.metric("Total 2025", get_value("Total 2025"))
col4.metric("% Change (2024 vs 2023)", get_value("% Change (2024 vs 2023)"))

st.divider()

# Load the month-wise traffic table
df = pd.read_excel(xls, table, skiprows=7)

df = df[df["Month"].isin(MONTH_ORDER)]
df["Month"] = pd.Categorical(df["Month"], categories=MONTH_ORDER, ordered=True)
df = df.sort_values("Month")

st.subheader("Monthly Data")
st.dataframe(df, use_container_width=True)

# Plot traffic trends with controlled chart height
st.subheader("Traffic Trend")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df["Month"], df["Year_2023"], marker="o", linewidth=2, label="2023")
ax.plot(df["Month"], df["Year_2024"], marker="o", linewidth=2, label="2024")
ax.plot(df["Month"], df["Year_2025"], marker="o", linewidth=2, label="2025")

ax.set_xlabel("Month")
ax.set_ylabel("Traffic")
ax.set_title("Traffic Trend by Year")
ax.legend()
ax.grid(alpha=0.3)

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig, use_container_width=True)

# Extract and display the insight section
insight_text = "Insight not available."

for i in range(len(raw)):
    if str(raw.iloc[i, 0]).strip().upper() == "INSIGHT":
        insight_text = "\n".join(
            raw.iloc[i + 1:i + 6, 0].dropna().astype(str).tolist()
        )
        break

st.subheader("Insight")
st.markdown(insight_text)
