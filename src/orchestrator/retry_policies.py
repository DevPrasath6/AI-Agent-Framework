# Retry/backoff utilities
def exponential_backoff(attempt):
    return min(2**attempt, 60)
