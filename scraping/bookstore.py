import pandas as pd
from bs4 import BeautifulSoup
import requests
from amazoncaptcha import AmazonCaptcha

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import csv
import time
import random
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.nytimes.com/books/best-sellers/"
req = requests.get(url)


soup = BeautifulSoup(req.content, 'html.parser')
t = soup.find_all(id ='site-content')
t = str(t).split(" ")

names = []
authors = []
prices = []
print_lengths = []
publishers = []
publish_dates = []
isbn = []

name_flag = False
author_flag = False
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}


count = 0
for i, x in enumerate(t):
    if "Amazon" in x:
        link= t[i-3]
        link = link[link.index("=")+2:-1]
        print (link)

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(link)



        pageSource = driver.page_source

        pageSource = pageSource[:pageSource.index('a-carousel-card rpi-carousel-attribute-card rpi-learn-more-card')]
        pageSource = pageSource.split()

        driver.close()
        prices.append(pageSource[pageSource.index('a-color-price">')+1])

        try:
            start = pageSource.index('book_details-publisher"></span>')
            while '<span>' not in pageSource[start]:
                start += 1
            if '</span>' in pageSource[start]:
                publishers.append(pageSource[start][pageSource[start].index('<span>')+6:pageSource[start].index('</span>')])
            else:
                publisher = pageSource[start][pageSource[start].index('<span>')+6:] + " "
                while '</span>' not in pageSource[start]:
                    start += 1
                    publisher += pageSource[start] + " "
                    publisher += pageSource[start][:pageSource[start].index('</span>')]


                if '</span>' in publisher:
                    publishers.append(publisher[:publisher.index('</span>')])
                else:
                    publishers.append(publisher)
        except:
            publishers.append('Penguin Publishing')


        start = pageSource.index('<span>Print')
        while 'rpi-attribute-value">' != pageSource[start]:
            start += 1
        try:
            print_lengths.append(pageSource[start+1][pageSource[start+1].index("<span>")+6:])
        except:
            print_lengths.append("100")

        start = pageSource.index('<span>Publication')
        while 'rpi-attribute-value">' != pageSource[start]:
            start += 1
        start += 1
        publish_date = pageSource[start][pageSource[start].index('<span>')+6:] + " "

        while '</span>' not in pageSource[start]:
            start += 1
            publish_date += pageSource[start] + " "

        publish_date += pageSource[start][:pageSource[start].index('</span>')]

        publish_date = publish_date[:publish_date.index('</span>')]
        publish_dates.append(publish_date)

        try:
            start = pageSource.index('<span>ISBN-13</span>')
            while 'rpi-attribute-value">' != pageSource[start]:
                start += 1
            start += 1
            isbn.append(pageSource[start][pageSource[start].index('<span>')+6:pageSource[start].index('</span>')])
        except:
            isbn.append("N/A")






    if name_flag:
        if "<" not in x:
            if x == '&amp;':
                name += '&' + " "
            else:
                name += x + " "
        else:
            name += x[:x.index("<")]
            names.append(name)
            name_flag = False
            name = ""

    if "name" in x:
        if "<" in x:
            name = x[x.index(">")+1:x.index("<")]
            names.append(name)
        else:
            name = x[x.index(">")+1:] + " "
            name_flag = True

    if author_flag:
        if "<" not in x:
            author += x + " "
        else:
            author += x[:x.index("<")]
            authors.append(author)
            author_flag = False
            author = ""

    if "author" in x:
        author = ""
        author_flag = True



print_lengths = [int(x) for x in print_lengths]
prices = [float(x[1:]) for x in prices]


print (names)
print (authors)
print (publishers)
print (prices)
print (print_lengths)
print (publish_dates)
print (isbn)

with open("values.csv", "w") as file:
    writer = csv.writer(file)
    for i in range(len(names)):
        arr = []
        arr.append(names[i])
        arr.append(authors[i])
        arr.append(publishers[i])
        arr.append(prices[i])
        arr.append(print_lengths[i])
        arr.append(isbn[i])
        writer.writerow(arr)
