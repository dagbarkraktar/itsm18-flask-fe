# Web-интерфейс для ITSM18
ITSM18 Frontend

## Скриншоты
Dashboard (flask, echarts.js, bootstrap)
![screenshot here](/screenshots/screenshot_dash_sm.png)

Hardware list (flask, bootstrap)
![screenshot here](/screenshots/screenshot_hw_list_sm.png)

## Установка (Flask в docker контейнере)

### Сборка docker image

```sh
$ docker build -t flask-itsm18-fe .
```

### Запуск контейнера

Необходимо также передать переменные: `MYSQL_ITSM18_USER`, `MYSQL_ITSM18_PASS`, `MYSQL_ITSM18_HOST` Это можно сделать через файл `env.list`, содержащий строки вида `VAR=VAL`. Например:

```
# MYSQL credentials
MYSQL_ITSM18_USER=xxxxxxxx
MYSQL_ITSM18_PASS=xxxxxxxx
MYSQL_ITSM18_HOST=xxx.xxx.xxx.xxx
```

```sh
$ docker run -d --name flask-itsm-fe -p 8040:80 -v $(pwd)/app:/app --env-file ~/env.list flask-itsm18-fe
```
