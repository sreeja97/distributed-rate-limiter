import time
import redis
from config_util import ConfigUtil

class DistributedLeakyBucketRateLimiter:
    def __init__(self, config_file='config.ini'):
        config_util = ConfigUtil(config_file)

        # Redis connection settings
        self.redis_host = config_util.get('RateLimiter', 'redis_host', fallback='localhost')
        self.redis_port = config_util.getint('RateLimiter', 'redis_port', fallback=6379)

        # Leaky bucket parameters
        self.capacity = config_util.getint('RateLimiter', 'capacity', fallback=100)
        self.rate_limit = config_util.getfloat('RateLimiter', 'rate_limit', fallback=1)
        self.window_size = config_util.getint('RateLimiter', 'window_size', fallback=60)

        # Initialize Redis connection
        self.redis = redis.StrictRedis(host=self.redis_host, port=self.redis_port, decode_responses=True)

    def _get_key(self, identifier):
        return f'leaky_bucket:{identifier}'

    def _update_tokens(self, key):
        current_time = int(time.time())
        last_update_time = int(self.redis.hget(key, 'last_update_time') or 0)

        # Calculate the number of tokens added since the last update
        time_elapsed = current_time - last_update_time
        tokens_to_add = time_elapsed * self.rate_limit

        # Update the last update time
        self.redis.hset(key, 'last_update_time', current_time)

        # Add tokens to the bucket
        current_tokens_str = self.redis.hget(key, 'tokens') or '0'

        try:
            current_tokens = int(float(current_tokens_str))
        except ValueError:
            current_tokens = 0

        new_tokens = max(0, current_tokens + tokens_to_add)
        self.redis.hset(key, 'tokens', str(new_tokens))

    def is_allowed(self, identifier, tokens=1):
        key = self._get_key(identifier)
        self._update_tokens(key)

        # Check if there are enough tokens to fulfill the request
        current_tokens_str = self.redis.hget(key, 'tokens') or '0'

        try:
            current_tokens = int(float(current_tokens_str))
        except ValueError:
            current_tokens = 0

        if current_tokens >= tokens:
            # Subtract the requested tokens from the bucket
            new_tokens = max(0, current_tokens - tokens)
            self.redis.hset(key, 'tokens', str(new_tokens))
            return True
        else:
            return False
