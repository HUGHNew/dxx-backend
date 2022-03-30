# 大学习后端爬虫

Flask 后端

API:
- `/user/add` 增加管理员帐号
- `/user/check/<name>` 查询 `<name>` 是否大学习
- `/user/time/<name>` 查询 `<name>` 大学习时间
- `/count/<string:cls>` 统计班级学习人数
- `/list/<string:cls>` 列出所有已学习人员

Docker images
- `git4docker/flask`
- `nginx:alpine`

init:`sudo docker network create backend`

docker run:
```bash
#!/bin/bash
sudo docker run --network backend \
  --rm -itd -v $(pwd)/flask:/flask \
  --name flask flask uwsgi /flask/uwsgi.ini
sudo docker run --network backend \
  --rm -d -v $(pwd)/ngx:/etc/nginx/conf.d \
  --name ngx -p 8000:80 nginx:alpine nginx -g 'daemon off;'
```

使用参考:<https://hughnash.top/blogs/Flask-uWSGI-in-Docker.html>