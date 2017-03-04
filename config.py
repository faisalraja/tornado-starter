import os
import redis
import bmemcached
from authomatic import Authomatic
from playhouse.db_url import connect
from lib.auth import provider

# env
is_local = os.getenv('PYCHARM_HOSTED') == '1'

# Generating random hex
# >>> import os,binascii
# >>> binascii.b2a_hex(os.urandom(32)).upper()
# Add under Settings -> Config Variables or below
cookie_secret = os.getenv('COOKIE_SECRET', '-- generate a random 64 hexa decimal here per project --')


auth = {
    'google': {
        'class_': provider.Google,

        # Provider type specific keyword arguments:
        'short_name': 2,  # use authomatic.short_name() to generate this automatically
        'consumer_key': os.getenv('GOOGLE_KEY'),
        'consumer_secret': os.getenv('GOOGLE_SECRET'),
        'scope': ['profile', 'email']
    }
}

# Rate limiting settings
# rate_limit = (200, 60) # 200 request / minute
# rate_limit = (10000, 3600) # 10000 request / hour
rate_limit = None


# database config
db_config = {
    'url': os.getenv(
        'DATABASE_URL', 'postgres://root:root@localhost:5432/dev').replace('postgres:', 'postgres+pool:'),
    'max_connections': 10,
    'stale_timeout': 600
}

project_name = 'Tornado Starter'

max_workers = 10
password_iterations = int(os.getenv('PASSWORD_ITERATIONS', 13))

# redis client
rc = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))

# memcache client
mc = bmemcached.Client(servers=[os.getenv('MEMCACHIER_SERVERS', '127.0.0.1:11211')],
                             username=os.getenv('MEMCACHIER_USERNAME'),
                             password=os.getenv('MEMCACHIER_PASSWORD'))

# db client
db = connect(**db_config)

# authomatic
authomatic = Authomatic(config=auth, secret=cookie_secret, debug=is_local)
