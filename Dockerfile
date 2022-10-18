FROM python:3.9-alpine

# Install Python 3
#RUN apk add --no-cache python3.9 py3.9-pip augeas-libs && rm -rf /var/cache/apk/*
RUN apk add --no-cache augeas-libs gcc && rm -rf /var/cache/apk/*

# make some useful symlinks that are expected to exist
#RUN if [[ ! -e /usr/bin/python ]];        then ln -sf /usr/bin/python3 /usr/bin/python; fi
#RUN if [[ ! -e /usr/bin/python-config ]]; then ln -sf /usr/bin/python3-config /usr/bin/python-config; fi
#RUN if [[ ! -e /usr/bin/pydoc ]];         then ln -sf /usr/bin/pydoc3 /usr/bin/pydoc; fi
#RUN if [[ ! -e /usr/bin/easy_install ]];  then ln -sf $(ls /usr/bin/easy_install*) /usr/bin/easy_install; fi
    
#RUN easy_install pip && pip install --upgrade --no-cache-dir pip
# Install and upgrade Pip
#RUN if [[ ! -e /usr/bin/pip ]]; then ln -sf /usr/bin/pip3 /usr/bin/pip; fi
ADD pip.conf /etc/pip.conf

# Install nginx
RUN apk add --update nginx && rm -rf /var/cache/apk/*
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
