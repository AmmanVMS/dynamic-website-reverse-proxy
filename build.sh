#!/bin/bash
#
# Build the docker image.
#

cd "`dirname \"$0\"`"

docker build --tag niccokunzmann/dynamic-website-reverse-proxy .
