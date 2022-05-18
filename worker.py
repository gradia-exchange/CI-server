from urllib.parse import quote

import redis
from rq import Worker, Queue, Connection


listen = ["default"]

encoded_password = quote("MXQenWA5B4htsQ@", safe="")
redis_url = f"redis://desmondbrown:{encoded_password}@redis-14955.c257.us-east-1-3.ec2.cloud.redislabs.com:14955"  # os.getenv("REDISTOGO_URL", "redis://localhost:6379")


conn = redis.from_url(redis_url)


if __name__ == "__main__":
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
