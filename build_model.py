'''
@author: patrick
'''
import csv
import milk
import numpy as np
import os

f = open('country_energy.csv', 'r')
csvrows = [r for r in csv.reader(f)]
print csvrows
frows = []
for r in csvrows:
   frows.append([float(x) for x in r[3:]])          
#frows = [ [float(x) for x in r[3:]] for r in csvrows]
print frows

features = np.vstack(frows)
labels = [r[2] for r in csvrows]

#confusion_matrix, names = milk.nfoldcrossvalidation(features, labels)
classifier = milk.defaultclassifier()
model = classifier.train(features, labels)
