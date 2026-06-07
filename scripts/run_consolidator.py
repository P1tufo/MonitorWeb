import os
import sys

# Asegurar que el script pueda encontrar los modulos de la raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_PATH
from db.consolidator import DataConsolidator


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/run_consolidator.py <folder_path>")
        return

    folder = sys.argv[1]
    with DataConsolidator(DB_PATH) as dc:
        dc.consolidate_folder(folder)

if __name__ == "__main__":
    main()
