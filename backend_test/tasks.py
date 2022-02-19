from __future__ import absolute_import
from backend_test.webhook import send_daily_menu
from celery.utils.log import get_task_logger
from backend_test.celery import app

logger = get_task_logger(__name__)




@app.task(bind=True, name="backend_test.tasks.send_slack_reminder")
def send_slack_reminder(self):
    send_daily_menu()
    print(f"Request: {self.request!r}")
