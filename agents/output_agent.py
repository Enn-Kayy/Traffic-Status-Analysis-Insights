import pandas as pd
import matplotlib.pyplot as plt
import os

def output_agent(state):

    # Define output directories for files and plots
    output_dir = "data/output"
    plot_dir = os.path.join(output_dir, "plots")

    # Ensure the plot directory exists before saving images
    os.makedirs(plot_dir, exist_ok=True)

    # Create an Excel writer to generate the final report
    writer = pd.ExcelWriter(
        f"{output_dir}/traffic_report.xlsx",
        engine="xlsxwriter"
    )

    # Iterate through each processed table
    for name, data in state["processed_tables"].items():
        df = data["monthly_df"]
        summary = data["summary"]
        insight = state["insights"].get(name, "Insight not available.")

        # Prepare worksheet name and register it with the writer
        sheet = name[:30]
        workbook = writer.book
        worksheet = workbook.add_worksheet(sheet)
        writer.sheets[sheet] = worksheet

        # Define commonly used cell formats
        header_fmt = workbook.add_format({
            "bold": True,
            "border": 1,
            "align": "center"
        })

        text_fmt = workbook.add_format({
            "text_wrap": True,
            "valign": "top"
        })

        number_fmt = workbook.add_format({
            "border": 1
        })

        # Adjust column widths for better readability
        worksheet.set_column("A:A", 10)
        worksheet.set_column("B:D", 14)
        worksheet.set_column("E:F", 16)
        worksheet.set_column("H:Q", 18)

        # Write high-level KPI summary at the top of the sheet
        worksheet.write_row("A1", ["Metric", "Value"], header_fmt)
        worksheet.write_row("A2", ["Total 2023", summary["total_2023"]])
        worksheet.write_row("A3", ["Total 2024", summary["total_2024"]])
        worksheet.write_row("A4", ["Total 2025", summary["total_2025"]])
        worksheet.write_row(
            "A5",
            ["% Change (2024 vs 2023)", summary["percent_change_2024"]]
        )

        # Write the month-wise data table below the KPI section
        table_start_row = 7
        df.to_excel(
            writer,
            sheet_name=sheet,
            startrow=table_start_row,
            index=False
        )

        # Apply formatting to table headers
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(table_start_row, col_num, col_name, header_fmt)

        # Freeze header row to make scrolling easier
        worksheet.freeze_panes(table_start_row + 1, 0)

        # Generate and save the traffic trend line chart
        plt.figure(figsize=(12, 6), dpi=150)
        plt.plot(df["Month"], df["Year_2023"], marker="o", label="2023")
        plt.plot(df["Month"], df["Year_2024"], marker="o", label="2024")
        plt.plot(df["Month"], df["Year_2025"], marker="o", label="2025")
        plt.legend()
        plt.title(name)
        plt.xticks(rotation=45)
        plt.tight_layout()

        img_path = f"{plot_dir}/{name}.png"
        plt.savefig(img_path)
        plt.close()

        # Insert the generated plot into the worksheet
        worksheet.insert_image(
            "H2",
            img_path,
            {"x_scale": 1.3, "y_scale": 1.3}
        )

        # Place the generated insight text below the data table
        insight_row = table_start_row + len(df) + 3
        worksheet.write(insight_row, 0, "INSIGHT", header_fmt)
        worksheet.merge_range(
            insight_row + 1, 0,
            insight_row + 6, 5,
            insight,
            text_fmt
        )

    # Save and close the Excel report
    writer.close()
    return state
