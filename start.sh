#!/bin/bash
source /www/wwwroot/api-brainlib.egadestaviano.my.id/.venv/bin/activate
gunicorn -w 3 -b 127.0.0.1:8003 app.main:app
