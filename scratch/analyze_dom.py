
import asyncio
import httpx
from bs4 import BeautifulSoup

async def find_large_elements():
    url = "http://localhost:8000/analytics?tab=ia"
    print(f"Analyzing DOM of {url}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url)
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            
            elements = []
            for tag in soup.find_all(True):
                size = len(str(tag))
                elements.append((tag.name, tag.get('id', ''), tag.get('class', []), size))
                
            elements.sort(key=lambda x: x[3], reverse=True)
            
            print("\nTop 15 largest elements in DOM:")
            for tag_name, tag_id, tag_class, size in elements[:15]:
                print(f"- <{tag_name} id='{tag_id}' class='{tag_class}'>: {size / 1024:.2f} KB")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(find_large_elements())
