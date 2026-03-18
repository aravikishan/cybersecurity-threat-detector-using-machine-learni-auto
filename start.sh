#!/bin/bash
set -e
echo "Starting Cybersecurity Threat Detector Using Machine Learning..."
uvicorn app:app --host 0.0.0.0 --port 9138 --workers 1
