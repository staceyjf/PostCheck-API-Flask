# Gunicorn configuration file
import os

max_requests = 1000
max_requests_jitter = 50

log_file = "-"

bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"

workers = 2
threads = workers

timeout = 120
