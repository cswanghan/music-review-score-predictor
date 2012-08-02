#!/usr/bin/env bash

if [[ $# < 3 ]] ; then
  echo "Usage: index-crawl.sh genre startPage endPage"
  exit 1
fi

genre=$1
strt=$2
end=$3
dest=mc-data/$genre
if [[ ! -d $dest ]] ; then
  mkdir -p $dest
fi

for i in `seq $strt $end`; do
  url="http://www.metacritic.com/browse/albums/genre/date/${genre}?view=condensed&page=$i"
  echo $url
  wget $url -nc -O $dest/page-$i.html
  sleep 5
done
