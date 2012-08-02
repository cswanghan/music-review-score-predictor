import csv
import sys

print sys.argv[1]
file = open(sys.argv[1], 'r')

stats = {}
procd = 0
correct = 0
classes = ['vg','g','f','p','vp']
for c in classes:
    stats[c] = {'tp':0, 'fp':0, 'fn':0}

for count, row in enumerate(csv.reader(file)):
    if count != 0 and row[4] and row[4] != '': # skip header
        predicted = row[4]
        actual = row[5]
        if actual in classes: classes.remove(actual)
        if predicted == actual:
            correct += 1
            stats[actual]['tp'] += 1
        else:
            stats[predicted]['fp'] += 1
            stats[actual]['fn'] += 1
            
        procd += 1
if procd == 0: sys.exit()
print stats
print 'total accuracy:', str(float(correct)/procd)

for c, counts in stats.iteritems():
    if c not in classes:
        recall = float(counts['tp'])/(counts['tp']+counts['fp'])
        prec = float(counts['tp'])/(counts['tp']+counts['fn'])
        print 'Class %s. precision: %f, recall: %f' % (c, prec, recall)
print "**************"
