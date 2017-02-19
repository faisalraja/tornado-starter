import os
import redis
import bmemcached

# env
is_local = os.getenv('PYCHARM_HOSTED') == '1'

# memcache
memcache = bmemcached.Client(servers=[os.getenv('MEMCACHIER_SERVERS', '127.0.0.1:11211')],
                             username=os.getenv('MEMCACHIER_USERNAME'),
                             password=os.getenv('MEMCACHIER_PASSWORD'))

# Generating random hex
# >>> import os,binascii
# >>> binascii.b2a_hex(os.urandom(32)).upper()
# Add under Settings -> Config Variables or below
cookie_secret = os.getenv('COOKIE_SECRET', '-- generate a random 64 hexa decimal here per project --')


# Rate limiting settings
# rate_limit = (200, 60) # 200 request / minute
# rate_limit = (10000, 3600) # 10000 request / hour
rate_limit = None


# database config
db = {
    'url': os.getenv(
        'DATABASE_URL', 'postgres://root:root@localhost:5432/dev').replace('postgres:', 'postgres+pool:'),
    'max_connections': 20,
    'stale_timeout': 600
}

project_name = 'Tornado Starter'

max_workers = 10


redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_conn = redis.from_url(redis_url)
