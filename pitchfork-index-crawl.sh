#!/usr/bin/env bash

if [[ $# < 2 ]] ; then
  echo "Usage: index-crawl.sh startPage endPage"
  exit 1
fi

for i in `seq $1 $2`; do
  url="http://pitchfork.com/reviews/albums/$i/"
  echo $url
  mkdir data/$i 
  wget $url -nc -O data/$i/$i-index.html
  python extract-urls.py $i
  sleep 2
done
