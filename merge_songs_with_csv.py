'''
Find clips and create new csv with all data

@author: patrick
'''
import csv
import os
import subprocess
import sys

def main(genre):
    csv_path = 'mc-data/' + genre + '/' + genre + '.csv'
    newcsv = open(genre + '.csv', 'w')
    reader = csv.reader(open(csv_path, 'r'))
    writer = csv.writer(newcsv)
    writer.writerow(['Artist', 'Album', 'Score', 'clip1', 'clip2'])
   
    datadir = os.path.join(os.getcwd(),'sevdig-data/track/preview/')
  
    missing = 0 
    for count, row in enumerate(reader):
        print 'missing:', missing
        if count == 0:
            continue
        
        artist = row[0]
        album = row[1]
        score = int(row[2])
        print row
           
        songdir = os.path.join(datadir, artist + '/' + album)
#        print songdir
        
        if not os.path.exists(songdir):
            songdir = os.path.join(datadir + '/' + genre, artist + '/' + album)
#            print songdir
            if not os.path.exists(songdir):
                missing = missing + 2
                continue
            
        mp3s = [os.path.join(songdir, x)
                for x in os.listdir(songdir) if x.endswith('.mp3')]
        if mp3s:
            print 'mp3s', mp3s, 'row', row
            row.extend(mp3s)
            writer.writerow(row)
        
    newcsv.close()
       
if __name__ == '__main__':
    main(sys.argv[1])
