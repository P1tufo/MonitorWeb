import sys
import pandas as pd
from core.excel_processor import ExcelProcessor

def test_parse(file_path):
    print(f"Reading {file_path} with ExcelProcessor")
    try:
        processor = ExcelProcessor(file_path)
        df = processor.process_file("scratch/temp_lx02.xlsx")
        
        if df is not None:
            print("Columns:", df.columns.tolist())
            print(df.head(5))
        else:
            print("Failed to process")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_parse(sys.argv[1])
