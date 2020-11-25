from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import TimeoutError


# Proxy for executing functions to unsure error catching and proper timeouts
# returns the result of executing the function if it's successful or False to 
# indicate that something went wrong
# A Result is one of 
# False and the Execption if something went wrong 
# or
# Ret and None
# A Ret is any value or object return by performing the function call
# Function, List(any), ?Int ->  Result
def safe_execution(func, args = [], timeout = 5):
    ret = False
    exception = None

    with ThreadPoolExecutor(max_workers=2) as executor:
        try:
            future = executor.submit(func, *args)
            ret = future.result(timeout=timeout)
        except Exception as e:
            exception = e

    return ret, exception