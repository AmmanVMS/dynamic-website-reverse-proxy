Dynamic Website Reverse Proxy
=============================

[![build-docker-image](https://github.com/AmmanVMS/dynamic-website-reverse-proxy/actions/workflows/build-docker-image.yml/badge.svg)](https://github.com/AmmanVMS/dynamic-website-reverse-proxy/actions/workflows/build-docker-image.yml)
[![tests](https://github.com/AmmanVMS/dynamic-website-reverse-proxy/actions/workflows/tests.yml/badge.svg)](https://github.com/AmmanVMS/dynamic-website-reverse-proxy/actions/workflows/tests.yml)

This is a tool to make local services served in a community network available to the outside internet.
The intention is to
1. lower the bar to create internet services
2. increase accessibility from inside and outside the community network and thus make services in the network more attractive

Using the Server
----------------

You create an HTTP service in the local community network.
Then, you go to this service installation for your community.

You put in your IP address, your server name and your port.
When you submit, your website should be available under the hostname you entered.

### Docker Image

The server is available as a docker image from [niccokunzmann/dynamic-website-reverse-proxy](https://hub.docker.com/r/niccokunzmann/dynamic-website-reverse-proxy).

    docker pull niccokunzmann/dynamic-website-reverse-proxy

Setting up a Server
-------------------

You can setup the server for your community in case the server is not there.
1. Install [docker](https://docs.docker.com/install).
   You will need a 64 bit computer.
   ```
   wget -O- https://get.docker.com | sh
   ```
2. Start the server replacing the configuration variables accordingly.
   ```
   docker run -p "80:80" -e "DOMAIN=MY-DOMAIN" -d --rm niccokunzmann/dynamic-website-reverse-proxy
   ```
   Now, the server should be available at http://localhost.
3. Once the server is available, you need to configure the router of yours to forward the traffic.
   I.e. this could be your internet gateway available at [http://192.168.0.1](http://192.168.0.1).
   Somewhere you can find the "Port Forwarding" (DE: Portfreigabe/Portweiterleitung)
   Here, you can configure the gateway to forward traffic
   - from port 80 to your IP on port 80 (HTTP)
   - from port 80 to your IP on port 443 (HTTPS)
4. Setup a domain name.
   In case you have just a home router, you can use e.g. http://selfhost.eu to get a free of charge dynamic domain name.
5. In order for other people to reach not only your domain name but also other services on this domain,
   you need to setup a cname record.
   - Example:
     You registered `quelltext.selfhost.eu` free of charge.
     Now, you pay 2€/year and you buy `quelltext.eu`.
     Then, you setup the CNAME record `*.quelltext.eu` to point to `quelltext.selfhost.eu`.
   - You can also contact @niccokunzmann in an issue if you like to use a domain named `my-community.quelltext.eu`.
   - Your community has a website e.g. `freifunk-potsdam.de`.
     They can setup `service.freifunk-potsdam.de` and `*.service.freifunk-potsdam.de` to point to your domain.
6. Configure your gateway (the router at your home) to update the IP address behind the domain name.
   Your gateway usually has a dyndns configuration which you can configure.
   This will update the registered dynamic domain name once your provider switches your IP address.

Once these steps are undergone, you should be able to access your server from the internet using your domain and
be able to register new clients.
Note that this looks like a lot bot this would be necessary for many more people to provide their services.
Once this is done, they have a much easier process to share their site.

Configuration
-------------

The configuration of the service is done via environment variables.
This is the configuration you should touch:

- `DOMAIN` default `localhost`  
  This is the domain your servers serves from.
  If DOMAIN is "test.freifunk.net", new a hostname "chocolate" is prepended so the website is served under "chocolate.test.freifunk.net".
- `NETWORK` default `10.0.0.0/8`  
  This is the network address of the accepted services.
  I.e. Freifunk in Potsdam covers `10.22.0.0/16`.
- `MAXIMUM_HOST_NAME_LENGTH` default `50`  
  This is the maximum length of a host name.
- `DEFAULT_SERVER` default `localhost:$PORT`  
  The website served for each hostname that is not registered.
  By default, this will be the overview page of the web app.
- `DEFAULT_DOMAINS` default ``  
  This is a comma separated list of domain forwards for the nginx proxy. Examples:
  - `service.example.com->http://localhost:9001` serves the page when the domain `service.example.com` is requested.
  - `service.example.com->http://172.16.0.21` serves `172.16.0.21` when the domain `service.example.com` is requested.
  - `test1.example.com->http://172.16.0.21,test2.example.com->http://172.16.0.21` serves `http://172.16.0.21` for the domains `test1.example.com` and `test2.example.com`.
- `PORT` default `9001`  
  This is the port on which the app listens for connections.
- `HTTP_PORT` default `80`  
  This is the port on which nginx listens for connections.
- `DEBUG` default `true`  
  Can be `true` or `false`.
  A flag to make the app output more details when a crash happens.

This is configuration you can touch:
- `DATABASE`  
  This is the place the data is stored when the service restarts.
  - default for the Python app is `` and nothing will be saved to a file.
  - default for the docker container is `/data/db.pickle` which holds the state of the proxy.
- `SOURCE_CODE`  
  This is the directory the currently running source code can be obtained from.
  - default for the Python app is the module directory.
  - default for the docker container is `/app`
- `NGINX_CONF`
  This is the path to the file with the replaced nginx configuration in it.
  - default is `/tmp/nginx.conf`.

Development
-----------


Run the server

    python3 -m dynamic_website_reverse_proxy

Build the server and run it 

    docker build --tag niccokunzmann/dynamic-website-reverse-proxy . && docker run -p "9000:80" -e "DOMAIN=localhost:9000" -it --rm niccokunzmann/dynamic-website-reverse-proxy

Now, you can reach your server under http://localhost:9000.

Run the tests

    tox

Related Work
------------

- [Diskussion im FreiFunk-Forum](https://forum.freifunk.net/t/lokale-webdienste-freigeben/18625)
- [Freifunk-Website-Proxy](https://github.com/Freifunk-Potsdam/freifunk-website-proxy) - this project's base

