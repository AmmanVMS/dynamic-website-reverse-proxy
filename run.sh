#!/bin/bash
#
# Build the docker image.
#

cd "`dirname \"$0\"`"

./build.sh

docker run -p "9000:80" -e "DOMAIN=localhost:9000" -it --rm niccokunzmann/dynamic-website-reverse-proxy
