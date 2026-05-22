
import asyncio
import httpx
import sys
import os
import re

async def analyze_large_html():
    url = "http://localhost:8000/analytics?tab=ia"
    print(f"Analyzing {url}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                html = resp.text
                print(f"Total Size: {len(html) / 1024 / 1024:.2f} MB")
                
                # Find all <script> tags and their contents
                scripts = re.findall(r'<script.*?id="(.*?)".*?>(.*?)</script>', html, re.DOTALL)
                
                script_sizes = []
                for script_id, content in scripts:
                    size = len(content)
                    script_sizes.append((script_id, size))
                
                # Sort by size descending
                script_sizes.sort(key=lambda x: x[1], reverse=True)
                
                print("\nTop 10 largest JSON/Script blocks:")
                for script_id, size in script_sizes[:10]:
                    print(f"- {script_id}: {size / 1024:.2f} KB")
                
            else:
                print(f"Error status: {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(analyze_large_html())
