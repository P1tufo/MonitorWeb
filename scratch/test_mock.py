import sqlite3
from unittest.mock import patch

def test_mock():
    test_db = sqlite3.connect(":memory:")
    original_connect = sqlite3.connect
    
    def mocked_connect(path, *args, **kwargs):
        if path == "fake.db":
            return test_db
        return original_connect(path, *args, **kwargs)

    with patch("sqlite3.connect", side_effect=mocked_connect):
        conn = sqlite3.connect("fake.db")
        print(f"Connected to fake.db: {conn}")
        conn2 = sqlite3.connect(":memory:")
        print(f"Connected to :memory:: {conn2}")

if __name__ == "__main__":
    test_mock()
