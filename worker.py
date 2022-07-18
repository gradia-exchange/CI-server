import argparse 

from distutils.sysconfig import get_config_h_filename
from urllib.parse import quote

import redis
from rq import Worker, Queue, Connection


listen = ["default"]

# PRODUCTION = "production"
# DEVELOPMENT = "development"

encoded_password = quote("MXQenWA5B4htsQ@", safe="")
redis_url = f"redis://desmondbrown:{encoded_password}@redis-14955.c257.us-east-1-3.ec2.cloud.redislabs.com:14955"  # os.getenv("REDISTOGO_URL", "redis://localhost:6379")


conn = redis.from_url(redis_url)
if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-m", "--mode", default=PRODUCTION, required=False, help="production vs development mode")
    # args = parser.parse_args()

    # debug = False 
    # if args.mode == DEVELOPMENT:
    #     debug = True 

    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
