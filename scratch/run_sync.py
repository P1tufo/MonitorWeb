import sys
import os
from pathlib import Path
import logging

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load config to memory
from core.db_config_manager import load_config_to_memory
load_config_to_memory()

# Import and run pipeline
from routes.sync import _run_sync_pipeline
print("Starting sync pipeline...")
_run_sync_pipeline()
print("Sync pipeline completed.")
