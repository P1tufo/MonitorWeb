import os

def wrap_iife(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # If already wrapped, skip
    if content.strip().startswith('(() => {') or content.strip().startswith('(function()'):
        return
        
    # Wrap in IIFE
    wrapped = f"(() => {{\n{content}\n}})();"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(wrapped)

wrap_iife('static/js/analytics.js')
wrap_iife('static/js/analytics_mb51.js')
wrap_iife('static/js/analytics_proyecciones.js')
print("Successfully wrapped in IIFE.")
