'''
Read song artist/album from csv, find corresponding clips, and extract
features using yaafe and the given yaafe spec.

@author: patrick
'''
import csv
import os
import subprocess
import sys
from IPython.utils.io import stderr

def build_yaafe_cmd(rate, feature_spec, song_args):
    cmd = ['/opt/yaafe/bin/yaafe', '-r ' + str(rate),
           '-f',  feature_spec]
    cmd.extend(song_args)
    print cmd
    return cmd
def main(genre, start_row, end_row, feature_spec):
    csv_path = 'mc-data/' + genre + '/' + genre + '.csv'
    reader = csv.reader(open(csv_path, 'r'))
 
    datadir = os.path.join(os.getcwd(),'sevdig-data/track/preview/')
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
            songs = None
            if os.path.exists(songdir):
                songs = [os.path.join(songdir, x)
                         for x in os.listdir(songdir) if x.endswith('.mp3')]
            if not songs:
               print 'No clips for ' + artist + ', ' + album 
               stats['missing'] = stats['missing'] + 2
               continue
           
            print 'extracting features for: ' + str(songs)
            print 'Attempt 1'
            proc = subprocess.Popen(
                build_yaafe_cmd(44100, feature_spec, songs),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (stdout, stderr) = proc.communicate()
            print 'return code %d' % proc.returncode
            print stderr.find('ERROR')
            if proc.returncode != 0 or stderr.find('ERROR') > -1:
                print "found error"
                if stderr.find('22050') > -1:
                    print "Attempt 2"
                    proc = subprocess.Popen(
                        build_yaafe_cmd(22050, feature_spec, songs),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    (stdout, stderr) = proc.communicate()
                    print proc.returncode
                    if proc.returncode != 0 or stderr.find('ERROR') > -1:
                        stats['errors'] = stats['errors'] + 2
                else:
                    print stderr
                    stats['errors'] = stats['errors'] + 2
            
           
    total = (end_row - start_row + 1) * 2
    processed = total - stats['missing'] - stats['errors']
    print 'Stats: total: %d, processed: %d, missing: %d, errors: %d' % (total,
        processed, stats['missing'], stats['errors'])
            
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " genre start_row end_row yaafe_feature_spec"
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
