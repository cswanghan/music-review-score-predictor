'''
Read artist/albums from csv and do search against 7 digital api.
Save responses in sevdig-data/release/search.

@author: patrick
'''
import codecs
import csv
import os
import random
import requests
import sys
import time

sevdig_api = 'http://api.7digital.com/1.2'
sevdig_key = '7dn46vx36ztn'

def artist_album_file_name(artist, album):
    return query.replace(' ', '_').replace('/', '') + '.xml'

def main(genre, start_row, end_row):
    csv_path = 'mc-data/' + genre + '/' + genre + '.csv'
    reader = csv.reader(open(csv_path, 'r'))
  
    datadir = 'sevdig-data/release/search/' + genre
    if not os.path.exists(datadir):
        os.makedirs(datadir)
        
    for count, row in enumerate(reader):
        if count == 0:
            continue
        if count >= start_row and count <= end_row:
            artist = row[0]
            album = row[1]
            print "row %d, artist: %s, album %s" % (count, artist, album)
            query = artist + ' ' + album
            r = requests.get(sevdig_api + '/release/search', params={'q': query,
                'country':'US', 'oauth_consumer_key':sevdig_key})
            print r.status_code
            filename = query.replace(' ', '_').replace('/', '') + '.xml'
            filepath = os.path.join(datadir, filename)
            file = codecs.open(filepath, 'w', 'utf-8')
            file.write(r.content)
            rate_headers = ['x-ratelimit-limit', 'x-ratelimit-current', 'x-ratelimit-reset']
            for h in rate_headers:
                print h + ": " + r.headers[h]
            sec = int(r.headers['x-ratelimit-reset'])
            min = sec / 60
            hrs = min / 60
            min = str(min % 60)
            if len(min) == 1: min = '0' + min
            print "time left till next period: %d:%s" % (hrs, min)
            time.sleep(random.randrange(3,7))
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " genre start_row end_row"
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
