from sqlalchemy import create_engine
db_path = "/Users/christianykelly/Desktop/MonitorWeb/Temp_Assets/memdb_test"
url = f"sqlite:///file:{db_path}?mode=memory&cache=shared&uri=true"
try:
    engine = create_engine(url, connect_args={"check_same_thread": False})
    with engine.connect() as conn:
        print("Succeeded without connect_args uri=True!")
except Exception as e:
    print("Failed without connect_args uri=True:", e)
