import urllib.request
import json
import re

def check_server():
    try:
        # Peticion a localhost
        req = urllib.request.Request('http://localhost:8000/')
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Buscar el tag de script que contiene data_wms_labels
            # o simplemente ver si la tabla contiene a CVALDERRAMA y 37
            
            if "CVALDERRAMA" in html and "37" in html:
                print("SERVER IS RETURNING CVALDERRAMA 37!")
            else:
                print("SERVER IS NOT RETURNING CVALDERRAMA 37. Must be browser cache.")
                
            # Extraer el json si existe
            match = re.search(r'<script type="application/json" id="data_ots_summary">(.*?)</script>', html, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                print("Found ots_summary with length:", len(data))
                
    except Exception as e:
        print("Could not connect to server:", e)

if __name__ == '__main__':
    check_server()
