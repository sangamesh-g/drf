from celery import shared_task
import time
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={'max_retries': 3},
    time_limit=60,
    soft_time_limit=50
)
def process_report(self, report_id):
    """
    Covers:
    - background execution
    - retry
    - redis usage
    - progress tracking
    - idempotency
    """

    lock_key = f"report:lock:{report_id}"

    # 🔐 IDEMPOTENCY (prevent duplicate processing)
    if redis_client.exists(lock_key):
        print("Already processed")
        return "Already processed"

    redis_client.set(lock_key, 1, ex=300)

    progress_key = f"report:progress:{self.request.id}"

    # 🧠 STEP 1
    redis_client.set(progress_key, 10)
    time.sleep(1)

    # 🧠 STEP 2 (simulate slow work)
    redis_client.set(progress_key, 40)
    time.sleep(2)

    # 🧠 STEP 3 (external API / ML / heavy loop)
    redis_client.set(progress_key, 70)
    time.sleep(2)

    # 🧠 FINAL STEP
    redis_client.set(progress_key, 100, ex=300)

    return {
        "report_id": report_id,
        "status": "processed"
    }
