import os
import memcache as mc

# env
is_local = os.environ.get('PYCHARM_HOSTED') == '1'

# memcache
mc_servers = os.environ.get('MEMCACHIER_SERVERS', '127.0.0.1:11211')
if '127.0.0.1' not in mc_servers:
    mc_servers = '{}:{}@{}'.format(os.environ.get('MEMCACHIER_USERNAME'),
                                   os.environ.get('MEMCACHIER_PASSWORD'),
                                   mc_servers)

memcache = mc.Client([mc_servers], debug=is_local)

# Generating random hex
# >>> import os,binascii
# >>> binascii.b2a_hex(os.urandom(32)).upper()
cookie_secret = '-- generate a random 64 hexa decimal here per project --'


# Rate limiting settings
# rate_limit = (200, 60) # 200 request / minute
# rate_limit = (10000, 3600) # 10000 request / hour
rate_limit = None


# database config
db = {
    'url': os.environ.get(
        'DATABASE_URL', 'postgres://root:root@localhost:5432/dev').replace('postgres:', 'postgres+pool:'),
    'max_connections': 20,
    'stale_timeout': 600
}

project_name = 'Tornado Starter'

max_workers = 10
