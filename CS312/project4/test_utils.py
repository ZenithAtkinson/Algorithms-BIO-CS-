import threading
from functools import wraps

import pytest


def timeout(timer):
    def decorator(func):
        @wraps(func)
        def new_func(*args):
            # Create a thread to run the test
            test_thread = threading.Thread(target=lambda: func(*args))
            test_thread.start()

            # Wait for the thread to complete with a timeout
            test_thread.join(timeout=timer)

            if test_thread.is_alive():
                pytest.fail(f"Test exceeded time limit of {timer} seconds")

        return new_func

    return decorator
