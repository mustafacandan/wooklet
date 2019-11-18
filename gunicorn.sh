#!/usr/bin/env bash

#gunicorn --certfile misc/ss_ssl/cert.pem --keyfile misc/ss_ssl/key.pem "app:create_app()" -w2 --reload --access-logfile - --bind 0.0.0.0:8000
gunicorn "app:create_app()" -w5 --reload --access-logfile - --bind 0.0.0.0:8000 --limit-request-line 0 --timeout 300
