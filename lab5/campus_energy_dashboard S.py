import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import logging


logging.basicConfig(
    filename="energy_dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        total = self.calculate_total_consumption()
        return f"Building: {self.name}, Total Consumption: {total} kWh"


class BuildingManager:
    def __init__(self, data_path="data/"):
        self.data_path = Path(data_path)

    def load_all_csv(self):
        master_df = []
        try:
            for file in os.listdir(self.data_path):
                if file.endswith(".csv"):
                    try:
                        df = pd.read_csv(self.data_path / file)
                        df["building"] = file.replace(".csv", "")
                        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                        df = df.dropna()
                        master_df.append(df)
                        logging.info(f"File Loaded: {file}")
                    except Exception:
                        logging.error(f"Corrupted file skipped: {file}", exc_info=True)

            if not master_df:
                raise FileNotFoundError("No valid CSV files found.")

            final_df = pd.concat(master_df, ignore_index=True)
            return final_df

        except Exception as e:
            logging.error("Failed to load dataset", exc_info=True)
            return pd.DataFrame()


    def calculate_daily_totals(self, df):
        return df.resample("D", on="timestamp")["kwh"].sum()

    def calculate_weekly_totals(self, df):
        return df.resample("W", on="timestamp")["kwh"].sum()

    def building_summary(self, df):
        summary = df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])
        summary.to_csv("building_summary.csv")
        return summary

   
    def generate_dashboard(self, df):
        try:
            daily = self.calculate_daily_totals(df)
            weekly = self.calculate_weekly_totals(df)
            building_avg = df.groupby("building")["kwh"].mean()

            fig, ax = plt.subplots(3, 1, figsize=(12, 16))

            # Line graph (daily consumption)
            ax[0].plot(daily.index, daily.values)
            ax[0].set_title("Daily Energy Consumption")
            ax[0].set_ylabel("kWh")

            # Bar chart (avg weekly usage)
            ax[1].bar(weekly.index, weekly.values)
            ax[1].set_title("Weekly Total Energy Usage")
            ax[1].set_ylabel("kWh")

            # Scatter plot (timestamp vs kWh)
            ax[2].scatter(df["timestamp"], df["kwh"], alpha=0.6)
            ax[2].set_title("Scatter Plot - Peak Consumption")
            ax[2].set_xlabel("Time")
            ax[2].set_ylabel("kWh")

            plt.tight_layout()
            plt.savefig("dashboard.png")
            plt.close()

            logging.info("Dashboard generated successfully.")

        except Exception as e:
            logging.error("Dashboard generation failed", exc_info=True)

    
    def export_outputs(self, df, summary):
        try:
            df.to_csv("cleaned_energy_data.csv", index=False)

            with open("summary.txt", "w") as f:
                f.write("Campus Energy Use Summary\n\n")
                f.write(f"Total Campus Consumption: {df['kwh'].sum()} kWh\n")
                f.write(f"Highest Consuming Building: {summary['sum'].idxmax()}\n")
                f.write("\nBuilding-wise Summary:\n")
                f.write(str(summary))

            logging.info("Summary report & cleaned CSV exported.")

        except Exception:
            logging.error("Export failed", exc_info=True)


def main():
    bm = BuildingManager()

    print("Loading data...")
    df = bm.load_all_csv()

    if df.empty:
        print("No valid dataset found. Check logs.")
        return

    print("Generating Aggregation...")
    summary = bm.building_summary(df)

    print("Creating Dashboard...")
    bm.generate_dashboard(df)

    print("Exporting Results...")
    bm.export_outputs(df, summary)

    print("\n✔ Capstone Completed Successfully!")
    print("Generated files:")
    print("- cleaned_energy_data.csv")
    print("- building_summary.csv")
    print("- summary.txt")
    print("- dashboard.png")


if __name__ == "__main__":
    main()
