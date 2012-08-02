#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys

if len(sys.argv) < 2:
    "Usage:"
    sys.exit(1)

page = sys.argv[1]

data_dir = 'data/' + page + '/'
f = open(data_dir + page + '-index.html', 'r')
out = open(data_dir + 'urls', 'w')

soup = BeautifulSoup(f)

#print soup.prettify()

main = soup.find("div", id="main")

#print main
lis = main.find_all("li")

rev_urls = set()
for li in lis:
    url = li.find("a")["href"]
    rev_urls.add(url)

for r in rev_urls:
    out.write(r + "\n")

out.close()

print rev_urls
