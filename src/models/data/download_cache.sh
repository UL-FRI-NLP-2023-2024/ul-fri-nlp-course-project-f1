#!/bin/bash

URL_CACHE="https://drive.usercontent.google.com/download?id=1-Dht7o2lEzRqcM-KYY0Bl1sX7N9V_XhZ&export=download&authuser=1&confirm=t"
URL_FAISS="https://drive.usercontent.google.com/download?id=1zJ3Fi9cFLcTbdM1k37CzTpfwe1pgd9tx&export=download&authuser=1&confirm=t"

FILE_CACHE="cache.zip"
FILE_FAISS="faiss.zip"

wget "$URL_CACHE" -O "$FILE_CACHE"
wget "$URL_FAISS" -O "$FILE_FAISS"

mkdir -p .
mkdir -p .

unzip "$FILE_CACHE" -d .
unzip "$FILE_FAISS" -d .

rm -f "$FILE_CACHE"
rm -f "$FILE_FAISS"

echo "Download and extraction complete."
