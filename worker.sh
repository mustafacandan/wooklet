#!/usr/bin/env bash
redis-cli flushall
celery -A app.tasks worker --loglevel=INFO --concurrency=1