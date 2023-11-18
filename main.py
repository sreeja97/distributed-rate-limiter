"""Module providing a function for time"""
import time


from DistributedLeakyBucketRateLimiter import DistributedLeakyBucketRateLimiter


if __name__ == "__main__":
    rate_limiter = DistributedLeakyBucketRateLimiter()

    USER_ID = "user789"

    # Attempt to make requests exceeding the rate limit without a sleep
    for _ in range(2000):
        if rate_limiter.is_allowed(USER_ID):
            print("Request allowed in main.py")
        else:
            print("Rate limit exceeded in main.py. Request rejected.")

        time.sleep(0.2)
