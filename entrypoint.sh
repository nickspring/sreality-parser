#!/bin/bash

# install poetry libs
cd /app/src/ || exit
poetry install -vvv

# run django migrations
echo "Run parser..."
scrapy crawl sreality

# run webserver
echo "Run webserver..."
uvicorn server:app --reload --host 0.0.0.0 --port 8080
