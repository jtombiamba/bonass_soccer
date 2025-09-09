import logging
import os
import sys

log = logging.getLogger("gunicorn_conf")
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s %(asctime)s %(name)s %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

workers = os.getenv("WEB_CONCURRENCY")

if workers is None:
    import multiprocessing

    workers = multiprocessing.cpu_count() * 2 + 1
log.info("Gunicorn will spawn {workers} worker", extra={"workers": workers})

bind = "0.0.0.0:5000"
# https://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod
worker_tmp_dir = "/dev/shm"  # nosec
chdir = "/opt/app"  # nosec
preload_app = True
errorlog = "-"
