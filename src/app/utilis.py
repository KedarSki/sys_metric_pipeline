from pathlib import Path
import pandas as pd
import json



class FileConverter:
    def __init__(self, json_file, csv_file):
        self.json_file = json_file
        self.csv_file = csv_file

def json_to_csv_parser(json_file, csv_file):
    try:
        with open(json_file, "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file path is incorrect or file does not exist!")
    
    try:
        if "data" in json_data and "result" in json_data["data"]:
            data = json_data["data"]["result"]
            rows = []
            
            for entry in data:
                    continue
    except Exception as e:
        raise IOError(f"Error writing to csv file: {e}")


        
        



# def csv_to_json_parser(json_file):
#     pass

def main():
    json_file = Path('data', "metrics.json")
    csv_file = Path('data', "metrics.csv")
    json_to_csv_parser(json_file, csv_file)

if __name__ == "__main__":
    main()