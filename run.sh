#!/bin/bash
#
# Build the docker image.
#

cd "`dirname \"$0\"`"

mkdir -p "./data"

./build.sh

docker run -p "80:80" \
	-e "DOMAIN=example.com" \
	-e "DEFAULT_DOMAINS=test1.example.com->http://172.16.0.1" \
	-v "`pwd`/data:/data" \
	-it --rm niccokunzmann/dynamic-website-reverse-proxy
