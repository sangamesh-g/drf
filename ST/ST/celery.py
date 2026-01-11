import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ST.settings')

app = Celery('ST')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

'''
1️⃣ CHECK REDIS (Is Redis running?)
Command
redis-cli ping

Expected output
PONG


✔ Redis is working
❌ No response → Redis not running

2️⃣ CHECK MESSAGE BROKER (RabbitMQ)
Command
rabbitmqctl status

Expected

Status info printed

No crash / error

✔ RabbitMQ is running
❌ Error → broker down

3️⃣ CHECK CELERY WORKER (Most important)
Command
celery -A project worker -l info

Expected output
connected to amqp://...
ready.


✔ Worker connected to broker
❌ No “ready” → problem

4️⃣ CHECK CELERY CAN TALK TO DJANGO
Create test task

tasks.py

from celery import shared_task

@shared_task
def ping_task():
    return "pong"

5️⃣ SEND TASK FROM DJANGO SHELL
python manage.py shell

from app.tasks import ping_task
ping_task.delay()

Expected in worker log
Task app.tasks.ping_task succeeded


✔ Celery → Django → Broker → Worker works

6️⃣ CHECK RESULT BACKEND (Redis)
python manage.py shell

result = ping_task.delay()
result.get(timeout=5)

Expected output
'pong'


✔ Redis backend working
❌ Hangs / error → Redis misconfigured

7️⃣ CHECK TASK STATUS
from celery.result import AsyncResult
AsyncResult(result.id).status


Expected:

SUCCESS

8️⃣ CHECK BROKER CONNECTION FROM CELERY
celery -A project status

Expected
worker@hostname: OK


✔ Broker reachable
❌ No workers → broker / worker issue

9️⃣ CHECK CELERY BEAT (Optional)
celery -A project beat

Expected
Scheduler: Sending due task


✔ Beat working

🔟 CHECK REDIS HAS CELERY DATA
redis-cli

SCAN 0 MATCH celery*


✔ Keys exist → Celery using Redis

🧠 ONE-LINE DEBUG MAP (MEMORIZE)
If this fails	Check this
Task not executing	Celery worker
Worker not starting	Broker
result.get() hangs	Redis
Scheduled task not firing	Beat
API slow	You forgot Celery
📝 FINAL SHORT NOTE (COPY THIS)

Redis: redis-cli ping → PONG
Broker: rabbitmqctl status
Worker: celery -A project worker -l info
Test task: task.delay()
Result: result.get()

x'''