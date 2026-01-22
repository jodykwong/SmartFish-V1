#!/bin/bash
# Celery Worker启动脚本

cd /home/sunrise/SmartFish

# 激活虚拟环境
source venv/bin/activate

# 启动Celery Worker
celery -A thinking.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --max-tasks-per-child=100 \
    --logfile=logs/celery.log
