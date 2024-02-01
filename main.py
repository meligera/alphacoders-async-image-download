import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os

with open('listy2.html', 'r', encoding='utf-8') as file:
    # Read the content of the file
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

image_links = soup.find_all('img', {'class': 'thumb', 'src': True})

# Extract the 'src' attribute from each link
image_urls = [link['src'] for link in image_links]
modified_links = [link.replace('thumbbig-', '') for link in image_urls]
print(modified_links, len(modified_links))


async def download_image(session, url, proxy_url):
    try:
        async with session.get(url, proxy=proxy_url) as response:
            content = await response.read()
            response.raise_for_status()  # This will raise an exception for non-2xx status codes
            
            filename = os.path.basename(url)
            filepath = os.path.join('pictures', filename)

            # Create the 'pictures' folder if it doesn't exist
            os.makedirs('pictures', exist_ok=True)

            with open(filepath, 'wb') as file:
                file.write(content)
            print(f'Downloaded: {filename}')
    except aiohttp.ClientError as e:
        print(f'Error downloading {url}: {e}')

async def main():
    proxy_url = "http://127.0.0.1:2081"
    
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url, proxy_url) for url in modified_links]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
