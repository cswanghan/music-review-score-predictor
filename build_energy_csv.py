'''

@author: patrick
'''
import csv
import os
import sys

def main(genre, start_row, end_row):
    csv_path = 'mc-data/' + genre + '/' + genre + '.csv'
    reader = csv.reader(open(csv_path, 'r'))
    
    feature_name = 'energy'
    datadir = os.path.join(os.getcwd(),'sevdig-data/track/preview/')
    out = open(genre + '_' + feature_name + '.csv', 'w')
    writer = csv.writer(out)
    stats = {}
    stats['missing'] = 0
    stats['errors'] = 0
    for count, row in enumerate(reader):
        if count == 0:
            continue
        if count >= start_row and count <= end_row:
            print "======================="
            print stats
            print "======================="
            artist = row[0]
            album = row[1]
            print "row %d, artist: %s, album %s" % (count, artist, album)
           
            songdir = os.path.join(datadir, artist + '/' + album)
            print songdir
            feature_csvs = None
            
            if os.path.exists(songdir):
                feature_csvs = [os.path.join(songdir, x)
                         for x in os.listdir(songdir) if x.endswith(feature_name + '.csv')]
            if not feature_csvs:
                print 'No %s features found for %s, %s' % (feature_name, artist, album) 
                stats['missing'] = stats['missing'] + 2
                continue
            
            f_reader = csv.reader(open(feature_csvs[0],'r'))
            features = []
            # skip first 5 lines
            for _ in range(5):
                f_reader.next() 
            for frow in f_reader:
                print frow
                features.append(frow[0])
                
            row.extend(features)
            writer.writerow(row)
            
    out.close()
           
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " genre start_row end_row"
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
