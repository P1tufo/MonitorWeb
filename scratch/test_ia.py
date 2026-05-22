
import asyncio
import httpx
import sys
import os

async def test_analytics_ia():
    url = "http://localhost:8000/analytics?tab=ia"
    print(f"Testing {url}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            
            if resp.status_code == 200:
                html = resp.text
                print(f"HTML Length: {len(html)}")
                
                # Check for IA section markers
                has_tab_ia = 'id="tab-ia"' in html
                has_scatter = 'id="scatterChart"' in html
                has_alerts = 'class="table-alerts"' in html
                has_error = 'class="error-banner"' in html
                
                print(f"Has tab-ia: {has_tab_ia}")
                print(f"Has scatterChart: {has_scatter}")
                print(f"Has table-alerts: {has_alerts}")
                print(f"Has error-banner: {has_error}")
                
                if has_error:
                    import re
                    match = re.search(r'⚠️ Error: (.*?)</div>', html, re.DOTALL)
                    if match:
                        print(f"Error Message found in HTML: {match.group(1).strip()}")
                
                # Check for JSON data injection
                has_data_scatter = 'id="data_scatter"' in html
                print(f"Has data_scatter JSON: {has_data_scatter}")
                
                if not has_tab_ia:
                    print("CRITICAL: tab-ia div not found in HTML!")
            else:
                print(f"Failed to load page. Status: {resp.status_code}")
                print(resp.text[:500])
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    # Wait a bit for server to be ready if just started
    import time
    time.sleep(2)
    asyncio.run(test_analytics_ia())
