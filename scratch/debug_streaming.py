import ollama
import time

MODEL_NAME = "qwen3.5:2b"
content = """import os
from typing import Final
BASE_DIR: Final[str] = os.path.dirname(os.path.abspath(__file__))
DB_PATH: Final[str] = os.getenv("DB_PATH", os.path.join(BASE_DIR, "data", "wms_transactions.db"))
"""

prompt = f"Actúa como Desarrollador Senior. Evalúa este código y sugiere mejoras:\n```python\n{content}\n```"

print(f"--- Probando Streaming con {MODEL_NAME} ---")
try:
    messages = [{'role': 'user', 'content': prompt}]
    stream = ollama.chat(model=MODEL_NAME, messages=messages, stream=True)
    
    response_text = ""
    start_time = time.time()
    for chunk in stream:
        if 'message' in chunk and 'content' in chunk['message']:
            text = chunk['message']['content']
            response_text += text
            print(text, end="", flush=True)
        else:
            print(f"\n[!] Chunk inusual detectado: {chunk}")
            
    print(f"\n\n--- Prueba finalizada en {time.time() - start_time:.2f}s ---")
    print(f"Longitud de respuesta: {len(response_text)} caracteres.")

except Exception as e:
    print(f"Error en la prueba: {e}")
