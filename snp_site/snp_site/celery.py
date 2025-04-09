import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snp_site.settings")

app = Celery("snp_site")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "my_task": {
        "task": "snp_site.tasks.myprint",
        "schedule": crontab(),
    },
}
