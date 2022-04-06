# 大学习后端爬虫

Flask 后端

API:
- `/user/add` 增加管理员帐号
- `/user/check/<name>` 查询 `<name>` 是否大学习
- `/user/time/<name>` 查询 `<name>` 大学习时间
- `/count/<string:cls>` 统计班级学习人数
- `/list/<string:cls>` 列出所有已学习人员

Docker images
- `git4docker/flask:backend`
- `nginx:alpine`

## 手动容器管理

init:`sudo docker network create backend`

docker run: 见[run.sh](run.sh)

使用参考:<https://hughnash.top/blogs/Flask-uWSGI-in-Docker.html>

## docker compose

```bash
docker compose up
# 后台启动/daemon
docker compose up -d
```

> 具体使用需要配置 `flask/account.json` 从该文件读取管理员帐号
> 格式参考 `flask/account_template.json`