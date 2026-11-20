#!/bin/sh
# Downloads goodbooks-10k (CC BY-SA 4.0) ratings and book metadata into work/.
set -e
mkdir -p work && cd work
for f in ratings.csv books.csv; do curl -sSfL -o "$f" "https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/$f"; done
echo "Downloaded to work/"
