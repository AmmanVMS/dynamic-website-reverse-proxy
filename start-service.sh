
mkdir -p /run/nginx

nginx -v
sleep 0.01

python3 -m dynamic_website_reverse_proxy

