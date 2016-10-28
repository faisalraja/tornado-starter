import os
import memcache as mc

# memcache client
memcache = mc.Client(['127.0.0.1:11211'], debug=True)

# env
is_local = os.environ.get('PYCHARM_HOSTED') == '1'


# Generating random hex
# >>> import os,binascii
# >>> binascii.b2a_hex(os.urandom(32)).upper()
cookie_secret = '-- generate a random 64 hexa decimal here per project --'

# Remember that memcache can be evicted
session_backend = 'mc_session'


# Rate limiting settings
# rate_limit = (200, 60) # 200 request / minute
# rate_limit = (10000, 3600) # 10000 request / hour
rate_limit = None


# database config | change to better path
db = '/tmp/sample.db'

project_name = 'Tornado Starter'