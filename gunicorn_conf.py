from multiprocessing import cpu_count

# Socket Path
bind = "unix:/home/aiagent/aiagent/gunicorn.sock"

# Worker Options
workers = cpu_count() + 1
worker_class = "uvicorn.workers.UvicornWorker"

# Logging Options
loglevel = "debug"
accesslog = "/home/aiagent/aiagent/access_log"
errorlog = "/home/aiagent/aiagent/error_log"
