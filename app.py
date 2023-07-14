import requests
import csv
import numpy as np
import pandas as pd
import os
import io
import os.path
import time
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def parse1(str):
    response = requests.get("https://n-katalog.ru/search?keyword=" + str)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a', {'class':'model-all-shops ib'}):
        url = "https://n-katalog.ru"+link.get('href')
        path = "waksoft‑susu‑ru"
        parse_linq(url)
        pickture(url, path)

def parse(str):   
    linq_list = []
    linq_name = ""
    linq_Gig = ""
    temp = []
    response = requests.get("https://n-katalog.ru/search?keyword=" + str)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a', {'class': 'model-all-shops ib'}):
        temp = parse_linq("https://n-katalog.ru" + link.get('href'))
        response2 = requests.get("https://n-katalog.ru" + link.get('href'))
        soup2 = BeautifulSoup(response2.content, 'html.parser')
        for link1 in soup2.findAll('div', {'class': 'page-title'}):
            linq_name = link1.get('data-title')
        for link2 in soup2.findAll('td', {'class':'op3'}):
            linq_Gig = link2.text
        for l in temp:
            linq_list.append([l, linq_name])
        print(linq_Gig)
        #linq_list.append(parse_linq("https://n-katalog.ru" + link.get('href')))
    
    return linq_list
    

def parse_linq(href):
    linq_list = []
    response = requests.get(href)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('a', {'class':'yel-but-2'}):
        linq_list.append(link.get('onmouseover').split(sep='"')[1])

    if(linq_list.count == 0):
        print("Товара нет в наличии!")
    else:
        for link in linq_list:
            print("https://n-katalog.ru" + link)
    return linq_list

#def parse_emptyLinq(count):
    #print("Столько товаров не было в наличии по вашему поиску -> ")
    #print(count)
def contains(temp):
    with io.open('WishList.csv', mode='a', newline='', encoding="utf-8") as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for l in file_reader:
            if l == temp:
                return True
        return False
def addWish(url):
    linq_price = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for link in soup.findAll('div', {'class':'page-title'}):
        linq_name = link.get('data-title')
    for link in soup.findAll(class_='where-buy-price'):
        linq_price.append(link.text.split()[0]+"р")
    temp = [url, linq_price[0], linq_name]
    if contains(temp) == False:
        with io.open('WishList.csv', mode='a', newline='', encoding="utf-8") as r_file:
            file_writer = csv.writer(r_file, delimiter=",")
            file_writer.writerow(temp)

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    urls = []
    for img in tqdm(soup.find_all("img")):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
    img_url = urljoin(url, img_url)
    try:
        pos = img_url.index("?")
        img_url = img_url[:pos]
    except ValueError:
        pass

    if is_valid(img_url):
        urls.append(img_url)
    return urls

def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, url.split("/")[-1])
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))

def pickture(url, path):
    imgs = get_all_images(url)
    for img in imgs:
        download(img, path)

def parse_pick(str):
    response = requests.get("https://n-katalog.ru/search?keyword=" + str)
    soup = BeautifulSoup(response.content, 'html.parser')

    link = soup.find('a', {'class':'model-all-shops ib'})

def main():
    a = input()
    a = a.replace(' ', '+')
    os.system("WinPy.py")
    pr = parse(a)
    with open('WishList.csv', 'r', encoding="utf-8") as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        print(*file_reader)

if __name__ == '__main__':
    main()

