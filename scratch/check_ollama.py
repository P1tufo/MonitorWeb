import ollama
try:
    res = ollama.list()
    print("Response type:", type(res))
    print("First model sample:", res.models[0] if res.models else "No models")
    if res.models:
        print("Keys/Attrs of model:", dir(res.models[0]))
except Exception as e:
    print("Error:", e)
