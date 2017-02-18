import os
import memcache as mc

memcache = mc.Client(['127.0.0.1:11211'], debug=True)

# env
is_local = os.environ.get('PYCHARM_HOSTED') == '1'

# Generating random hex
# >>> import os,binascii
# >>> binascii.b2a_hex(os.urandom(32)).upper()
cookie_secret = '-- generate a random 64 hexa decimal here per project --'


# Rate limiting settings
# rate_limit = (200, 60) # 200 request / minute
# rate_limit = (10000, 3600) # 10000 request / hour
rate_limit = None


# database config
db_connection = os.environ.get(
    'DATABASE_URL', 'postgres://root:root@localhost:5432/dev').replace('postgres:', 'postgres+pool:')

project_name = 'Tornado Starter'

max_workers = 10
