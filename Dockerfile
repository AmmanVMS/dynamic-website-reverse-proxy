FROM alpine

# Install packages
RUN apk add --no-cache python3 py3-pip augeas-libs certbot nginx && rm -rf /var/cache/apk/*

# make pip also use piwheels
ADD pip.conf /etc/pip.conf

RUN chown -R nginx:www-data /var/lib/nginx

EXPOSE 80 443

# Create app environment
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED=true

# Create volume for persistence
ENV VOLUME=/data
ENV DATABASE=$VOLUME/db.pickle
RUN mkdir $VOLUME
VOLUME $VOLUME

# Install Packages
ADD requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]

# add source files
ENV SOURCE_CODE="/app"
ADD LICENSE .
ADD Dockerfile.license .
ADD Dockerfile .
ADD start-service.sh .

# Add the app
ADD dynamic_website_reverse_proxy dynamic_website_reverse_proxy
