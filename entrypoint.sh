#!/bin/sh
# Start Uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8080