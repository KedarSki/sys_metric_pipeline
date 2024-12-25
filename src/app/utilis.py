from pathlib import Path
import pandas as pd
import json


class FileConverter:
    def __init__(self, json_file, cpu_csv, ram_csv, disc_csv):
        self.json_file = json_file
        self.cpu_csv = cpu_csv
        self.ram_csv = ram_csv
        self.disc_csv = disc_csv

    def json_to_csv_parser(self):

        try:
            with open(self.json_file, "r") as file:
                json_data = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("JSON file path is incorrect or file does not exist!")

        try:
            if json_data.get("status") == "success":
                if "data" in json_data and "result" in json_data["data"]:
                    data = json_data["data"]["result"]
                    cpu_rows_list = []
                    ram_rows_list = []
                    disc_read_write_list = []

                    for entry in data:
                        if entry["metric"].get("__name__") == "node_cpu_seconds_total":
                            cpu_rows_list.append(
                                {
                                    "instance_id": entry["metric"]["instance"],
                                    "cpu": entry["metric"]["cpu"],
                                    "mode": entry["metric"]["mode"],
                                    "time_of_usage": entry["value"][1],
                                    "date": entry["value"][0],
                                }
                            )

                        elif entry["metric"].get("__name__") == "node_memory_Active_bytes":
                            ram_rows_list.append(
                                {
                                    "instance_id": entry["metric"]["instance"],
                                    "ram_usage": entry["value"][1],
                                    "date": entry["value"][0],
                                }
                            )

                        elif entry["metric"].get("__name__") == "node_disk_io_time_seconds_total":
                            disc_read_write_list.append(
                                {
                                    "instance_id": entry["metric"]["instance"],
                                    "device": entry["metric"]["device"],
                                    "usage": entry["value"][1],
                                    "date": entry["value"][0],
                                }
                            )

                    """
                    Write CPU data to CSV
                    """

                    if cpu_rows_list:
                        pd.DataFrame(cpu_rows_list).to_csv(self.cpu_csv, index=False)
                        print(f"CPU data saved to {self.cpu_csv}")

                    """
                    Write RAM data to CSV
                    """

                    if ram_rows_list:
                        pd.DataFrame(ram_rows_list).to_csv(self.ram_csv, index=False)
                        print(f"RAM data saved to {self.ram_csv}")

                    """
                    Write DISC data to CSV
                    """

                    if disc_read_write_list:
                        pd.DataFrame(disc_read_write_list).to_csv(self.disc_csv, index=False)
                        print(f"DISC data saved to {self.disc_csv}")

        except Exception as e:
            raise IOError(f"Error writing to csv file: {e}")


def main():
    base_dir = Path(__file__).parent / "../data"
    json_file = base_dir / "metrics.json"
    cpu_csv = base_dir / "CPU.csv"
    ram_csv = base_dir / "RAM.csv"
    disc_csv = base_dir / "DISC.csv"

    converter = FileConverter(json_file, cpu_csv, ram_csv, disc_csv)
    converter.json_to_csv_parser()


if __name__ == "__main__":
    main()
