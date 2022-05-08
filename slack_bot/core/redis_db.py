import os
import redis as r

redis_client = r.Redis(
  host=os.environ['REDIS_DB_HOST'],
  port=os.environ['REDIS_DB_PORT'],
  password=os.environ['REDIS_DB_PASSWORD'],
  username=os.environ['REDIS_DB_USERNAME']
)
