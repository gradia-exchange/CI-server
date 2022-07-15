import argparse 

from distutils.sysconfig import get_config_h_filename
from urllib.parse import quote

import redis
from rq import Worker, Queue, Connection


listen = ["default"]

PRODUCTION = "production"
DEVELOPMENT = "development"

encoded_password = quote("MXQenWA5B4htsQ@", safe="")
redis_url = f"redis://desmondbrown:{encoded_password}@redis-14955.c257.us-east-1-3.ec2.cloud.redislabs.com:14955"  # os.getenv("REDISTOGO_URL", "redis://localhost:6379")


def get_connection(debug=False):
    if debug:
        return redis.from_url("redis://localhost:6379")
    return redis.from_url(redis_url)


conn = get_connection()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", default=PRODUCTION, required=False, help="production vs development mode")
    args = parser.parse_args()

    debug = False 
    if args.mode == DEVELOPMENT:
        debug = True 

    conn = get_connection(debug=debug)
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
