# 📊 Traffic Status Analysis & Insight Dashboard

## 📌 Project Overview

The **Traffic Status Analysis & Insight Dashboard** is an end-to-end data analytics project designed to analyze website traffic data across multiple years, calculate meaningful performance metrics, generate management-level insights, and present results through both an Excel report and an interactive dashboard.

The project follows an **agent-based architecture** using **LangGraph**, where each agent is responsible for a specific stage of data processing. The final output is a clean, decision-ready report suitable for business and management use.

---

## 🎯 Objectives

- Analyze month-wise traffic data for multiple years (2023, 2024, 2025)
- Calculate key performance metrics such as:
  - Year-over-Year (YoY) growth
  - Month-over-Month (LM) change
  - Annual totals and percentage change
- Generate professional, management-focused insights
- Export results to a well-formatted Excel report with charts
- Visualize data and insights using a Streamlit dashboard

---

## 🧠 Architecture Overview

The project uses a **LangGraph-based pipeline**, where each processing step is implemented as an independent agent:


Each agent receives and updates a shared state object, ensuring a clean and modular workflow.

---

## 🧩 Agents Description

### 1️⃣ Input Agent
- Reads the input Excel file containing multiple traffic tables
- Validates required columns
- Converts yearly values into numeric format
- Stores cleaned tables in shared state

### 2️⃣ Metrics Agent
- Cleans and orders month-wise data
- Calculates:
  - YoY % change (2024 vs 2023)
  - LM % change for 2024
  - Annual totals for each year
- Prepares summary statistics for reporting

### 3️⃣ Insight Agent
- Analyzes overall annual growth trends
- Determines whether performance reflects growth, decline, or stability
- Generates professional, management-level insights focused on:
  - Overall performance direction
  - Strategic interpretation
  - High-level recommendations

### 4️⃣ Output Agent
- Generates a formatted Excel report
- Adds:
  - KPI summary section
  - Month-wise tables
  - High-resolution line charts
  - Insight text for each table
- Saves all plots and embeds them into the Excel file

---

## 📊 Dashboard (Streamlit)

The Streamlit dashboard provides an interactive interface to:

- Select and view different traffic tables
- Display KPI metrics (Totals & % Change)
- View month-wise traffic trends with properly scaled charts
- Read management-level insights directly from the report

---

## 📁 Project Structure


Each agent receives and updates a shared state object, ensuring a clean and modular workflow.

---
## 📁 Project Structure
```
Traffic Status/
│
├── agents/
│ ├── input_agent.py
│ ├── metrics_agent.py
│ ├── insight_agent.py
│ └── output_agent.py
│
├── graph/
│ ├── state.py
│ └── traffic_graph.py
│
├── dashboard/
│ └── app.py
│
├── data/
│ ├── input/
│ │ └── traffic_input.xlsx
│ └── output/
│ ├── traffic_report.xlsx
│ └── plots/
│
├── main.py
├── .env
└── README.md
```

---

## ⚙️ Technologies Used

- **Python**
- **Pandas** – Data processing and calculations
- **Matplotlib** – Graph generation
- **Streamlit** – Interactive dashboard
- **LangGraph** – Agent-based workflow orchestration
- **XlsxWriter** – Excel formatting and report generation
- **dotenv** – Environment variable management

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

## ▶️ How to Run the Project

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
``` 

### Step 2: Run the main script
```bash
python main.py
```

### Step 3: View the dashboard
```bash
streamlit run dashboard/app.py
```


