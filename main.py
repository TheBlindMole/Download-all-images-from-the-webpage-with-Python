"""
This code does not work if the browser uses JavaScript to inject the imgs

import os 
import requests
from bs4 import BeautifulSoup

print("Write the webpage URL here:")
url = input
def imagedown(url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

images = soup.find_all('img')

print(images)

for image in images:
    name = image.get('alt', 'sem_nome')
    link = image['src']
    with open (name.replace (' ', '-').replace('/', ' ') + '.jpg', 'wb') as f:
        im = requests.get(link)
        f.write(im.content)
        print('Writing:', name) 
        imagedown(url, 'img')
"""

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Link to the desired web page
url = 'https://www.ign.com/wikis/the-legend-of-zelda-breath-of-the-wild/All_Recipes_and_Cookbook'
folder_name = 'img'

os.makedirs(folder_name, exist_ok=True)

# Headers to pretend to be a real web browser and avoid basic blocks
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

print("Downloading page content...")
r = requests.get(url, headers=headers)

if r.status_code != 200:
    print(f"Error accessing the site. Status code: {r.status_code}")
else:
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')

    print(f"Total images found: {len(images)}")

    for index, image in enumerate(images):
        # 'data-src' or 'srcset' for lazy loading
        link = image.get('src') or image.get('data-src')
        
        if not link:
            continue
        
        # Ignore small icons or avatars
        if 'avatar' in link or 'icon' in link:
            continue

        link = urljoin(url, link)
        
        name = image.get('alt', f'image_{index}')
        if not name.strip():
            name = f'image_{index}'
            
        safe_name = name.replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_').strip()
        file_path = os.path.join(folder_name, f"{safe_name}.jpg")
        
        try:
            im = requests.get(link, headers=headers)
            if im.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(im.content)
                print(f'Saved: {safe_name}.jpg')
            else:
                print(f'Failed to download (Status {im.status_code}): {link}')
        except Exception as e:
            print(f'Error downloading {link}: {e}')
