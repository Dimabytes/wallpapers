import requests 
import random
from lxml import html
import glob
import os
base_url = 'https://wallpaperscraft.ru'

files = glob.glob('wallpapers/*.jpg')
for f in files:
    os.remove(f)
keywords = {'nature': 989, 'textures': 179}
links = []
wallpapers = []
print('Open categories...')
for keyword in keywords:
    link = base_url + '/catalog/' + keyword + '/page' + str(random.randint(2, keywords[keyword]))
    response = requests.get(link)
    parsed_body = html.fromstring(response.text)
    all_links = parsed_body.xpath('//a/@href')
    print('Open ' + link)
    for link in all_links:
        if '/wallpaper/' in link:
            links.append(link)
print('Creating download links...')
for wallpaper in links:
    link = base_url + wallpaper
    response = requests.get(link)
    parsed_body = html.fromstring(response.text)
    all_links = parsed_body.xpath('//a/@href')
    for i in all_links:
        if '1920x1080' in i:
            i = i.replace('/1920', '_1920')
            i = i.replace('download', 'image')
            i = base_url + i + '.jpg'
            wallpapers.append(i)
print('Start download')
for wallpaper in wallpapers:
    name = 'wallpapers/' + str(random.random()) + '.jpg'
    with open(name, 'wb') as handle:
        response = requests.get(wallpaper, stream=True, allow_redirects=True)

        if not response.ok:
            print (response)
        else:
            print('downloading... ' + wallpaper)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
