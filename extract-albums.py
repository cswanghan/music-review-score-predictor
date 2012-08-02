#!/usr/bin/env python
from bs4 import BeautifulSoup
import sys
import os
from datetime import datetime
import unicodedata
import re
from review import Review
from pymongo import Connection

def arff_escape(val):
    # replace all nonascii characters
    val = unicodedata.normalize('NFKD', val).encode('ascii', 'ignore')
    return val.replace("'", "\\'").replace('\n',' ')

if len(sys.argv) < 3:
    "Usage:"
    sys.exit(1)

start = int(sys.argv[1])
end = int(sys.argv[2])

#out = open('data/%d-%d-albums.arff' % (start, end) , 'w')
#out.write(Review().arff_header())

connection = Connection()
db = connection.pitchfork

count = 0
for cur in range(start, end):
    print 'page: ' + str(cur)
    data_dir = 'data/' + str(cur) + '/'
    paths = os.listdir(data_dir)

    paths = [relpath for relpath in paths if \
        relpath.find('index.html') == -1 and \
        relpath != "urls" and relpath.find('.arff') == -1]

    for relpath in paths:
        path = data_dir + relpath
        print path
        soup = BeautifulSoup(open(path))
        try:
            meta = soup.find('ul', {"class":"review-meta"})
            rev = Review()
            rev.id = int(re.search('\d+', relpath).group(0))
            rev.artist = meta.find('h1').find('a').get_text()
            rev.album = meta.find('h2').get_text()
            str_date = meta.find('span', {"class":"pub-date"}).get_text()
            rev.date = datetime.strptime(str_date, '%B %d, %Y')
            rev.score = float(meta.find('span', {"class":"score"}).get_text())
            rev.text = soup.find('div', {"class":"editorial"}).get_text()

            db.reviews.insert(rev.__dict__)
            count = count + 1
            print count 
            #out.write(rev.arff_row())

            #print str(rev)
        except Exception as e:
            print e
            print 'failed to parse ' + path

#out.close()

