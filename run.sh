#!/bin/bash
#
# Build the docker image.
#

cd "`dirname \"$0\"`"

./build.sh

docker run -p "80:80" -e "DOMAIN=test.localhost" -it --rm niccokunzmann/dynamic-website-reverse-proxy
