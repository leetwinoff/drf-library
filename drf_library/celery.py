import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_library.settings")

app = Celery("drf_library")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.broker_url = "redis://localhost:6379/0"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
