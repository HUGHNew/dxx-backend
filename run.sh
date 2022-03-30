#!/bin/bash
sudo docker run --network backend --rm -itd -v $(pwd)/flask:/flask  --name flask git4docker/flask:backend
sudo docker run --network backend --rm -d -v $(pwd)/ngx:/etc/nginx/conf.d --name ngx -p 8000:80 nginx:alpine nginx -g 'daemon off;'