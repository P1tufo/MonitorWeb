import re

def extract_body(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract inner content of analytics-container, skipping the header
    match = re.search(r'<div class="analytics-container">.*?</header>(.*?)</div>\s*(?:{% include|<!-- Inject|</body>|<script)', content, re.DOTALL | re.IGNORECASE)
    if match:
        body = match.group(1).strip()
    else:
        body = ""
        
    # Extract script data variables and js files carefully
    # Find all <script> and <!-- --> tags at the end of the body
    scripts = ""
    scripts_match = re.findall(r'(<script[^>]*>.*?</script>|<!--.*?-->)', content, re.DOTALL | re.IGNORECASE)
    
    valid_scripts = []
    for s in scripts_match:
        if 'cdn.jsdelivr.net' not in s and 'chart.js' not in s:
            valid_scripts.append(s)
            
    # Also find any data variables or JS includes that are after modals
    scripts = "\n".join(valid_scripts)
    
    return body, scripts

def main():
    vl06o_body, vl06o_scripts = extract_body('scratch/analytics.html.bak')
    mb51_body, mb51_scripts = extract_body('templates/analytics_mb51.html')
    ia_body, ia_scripts = extract_body('templates/analytics_proyecciones.html')
    
    # Rename variables in MB51 HTML
    mb51_body = mb51_body.replace('top_materials', 'mb51_top_materials')
    mb51_scripts = mb51_scripts.replace('top_materials', 'mb51_top_materials')
    mb51_scripts = mb51_scripts.replace('{{ area_stats_json', '{{ mb51_area_stats_json')
    mb51_scripts = mb51_scripts.replace('{{ area_material_mapping', '{{ mb51_area_material_mapping')
    mb51_scripts = mb51_scripts.replace('{{ user_material_mapping', '{{ mb51_user_material_mapping')
    mb51_scripts = mb51_scripts.replace('{{ ubicaciones_mapping', '{{ mb51_ubicaciones_mapping')
    
    # Filter out scripts to only include local js files and data tags
    def filter_scripts(scripts_str):
        lines = []
        for line in scripts_str.split('\n'):
            if 'script type="application/json"' in line or 'src="{{ url_for' in line or '<!-- Inject' in line:
                lines.append(line)
        return "\n".join(lines)
        
    vl06o_scripts = filter_scripts(vl06o_scripts)
    mb51_scripts = filter_scripts(mb51_scripts)
    ia_scripts = filter_scripts(ia_scripts)
    
    new_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secciones Consolidadas | Proyecto</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    {{% include "partials/_styles.html" %}}
    <link rel="stylesheet" href="{{{{ url_for('static', path='css/analytics.css') }}}}">
    <link rel="stylesheet" href="{{{{ url_for('static', path='css/analytics_mb51.css') }}}}">
    <link rel="stylesheet" href="{{{{ url_for('static', path='css/analytics_proyecciones.css') }}}}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0"></script>
    <style>
        .tabs-header {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding-bottom: 1rem;
            flex-wrap: wrap;
        }}
        .tab-btn {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            color: #cbd5e1;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
            font-family: inherit;
        }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.1); }}
        .tab-btn.active {{
            background: rgba(93,186,169,0.2);
            color: #5DBAA9;
            border-color: rgba(93,186,169,0.5);
        }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
    </style>
</head>
<body>
    <div class="analytics-container">
        <header class="main-header">
            <div class="header-top">
                <div class="logo-group">
                    <h1>Analíticas Consolidadas</h1>
                    <p class="header-desc">KPIs Operativos, Movimientos y Proyecciones IA</p>
                </div>
                <div class="actions">
                    <a href="/" class="btn btn-secondary">🏠 Dashboard</a>
                </div>
            </div>
        </header>

        <div class="tabs-header">
            <button class="tab-btn active" onclick="switchTab('vl06o', this)">📊 VL06o (Entregas)</button>
            <button class="tab-btn" onclick="switchTab('mb51', this)">📦 MB51 (Movimientos)</button>
            <button class="tab-btn" onclick="switchTab('ia', this)">🧠 IA Predictiva</button>
        </div>

        <div id="tab-vl06o" class="tab-content active">
{vl06o_body}
        </div>

        <div id="tab-mb51" class="tab-content">
{mb51_body}
        </div>

        <div id="tab-ia" class="tab-content">
{ia_body}
        </div>
    </div>

    {{% include "partials/_analytics_modals.html" %}}
    {{% include "partials/_analytics_mb51_modals.html" %}}
    {{% include "partials/_analytics_proyecciones_modals.html" %}}

    <script>
        function switchTab(tabId, btnElement) {{
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById('tab-' + tabId).classList.add('active');
            btnElement.classList.add('active');
            // Trigger resize so Chart.js renders correctly inside newly visible containers
            window.dispatchEvent(new Event('resize'));
        }}
    </script>

{vl06o_scripts}
{mb51_scripts}
{ia_scripts}

</body>
</html>
"""
    with open('templates/analytics.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

if __name__ == '__main__':
    main()
