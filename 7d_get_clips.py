'''
@author: patrick
'''
import codecs
import csv
from lxml import etree
import os
import properties
import random
import requests
import sys
import time

MAX_TRIES = 6
MAX_DOWNLOADS = 2

def main(genre, start, end):
   
    indatadir = 'sevdig-data/release/tracks/' + genre
    outdatadir = 'sevdig-data/track/preview/' + genre 
   
    total = len(os.listdir(indatadir))
    for count, search_file_name in enumerate(sorted(os.listdir(indatadir))):
        if count >= start and count <= end:
            print 'processing release %d/%d' % (count, total)
            xmlstr = codecs.open(os.path.join(indatadir, search_file_name), 'r', 'utf-8').read()
            # lxml doesn't like the encoding for some reason
            xmlstr = xmlstr.replace(' encoding="utf-8"', '')
            root = etree.fromstring(xmlstr)
            tracks = root.findall('tracks/track')
            
            artist = tracks[0].find('release/artist/name').text
            album = tracks[0].find('release/title').text
            
            downloaded_count = 0
            try_count = 0
            
            for count, track in enumerate(tracks):
                if downloaded_count >= MAX_DOWNLOADS or count > MAX_TRIES:
                    break
                
                mp3_dir = os.path.join(outdatadir, artist + '/' + album)
                if not os.path.exists(mp3_dir):
                    print 'creating ' + mp3_dir
                    os.makedirs(mp3_dir)
                 
                track_id = track.get('id')
                title = track.find('title').text
                r = requests.get(properties.sevdig_api+'/track/preview', 
                    params={'trackid': track_id, 
                    'oauth_consumer_key': properties.sevdig_key, 'country': 'US'})
                mp3_name = track_id + '.mp3'
                print 'downloading ' + track_id + ' ' + title
                   
                mp3_file = open(os.path.join(mp3_dir, mp3_name), 'wb')
                mp3_file.write(r.content)
                mp3_file.close()
                downloaded_count = downloaded_count + 1
                
#                rate_headers = ['x-ratelimit-limit', 'x-ratelimit-current',
#                                'x-ratelimit-reset']
#                
#                for h in rate_headers:
#                    print h + ": " + r.headers[h]
#                sec = int(r.headers['x-ratelimit-reset'])
#                min = sec / 60
#                hrs = min / 60
#                min = str(min % 60)
#                if len(min) == 1: min = '0' + min
#                print "time left till next period: %d:%s" % (hrs, min)
                print r.headers
                time.sleep(random.randrange(2,3))
                #time.sleep(random.randrange(3,7))
        
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " genre start_row end_row"
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
