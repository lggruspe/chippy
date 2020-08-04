"""Stabilize clock rate."""

import time

def stabilize_frame(period, *functions):
    """Sleep if the functions don't use up the entire frame period.

    Return elapsed time in functions.
    """
    start_time = time.time()
    for f in functions:
        f()
    elapsed = time.time() - start_time
    remaining = period - elapsed
    if remaining > 0:
        time.sleep(remaining)
    return elapsed
