from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import TimeoutError

import json

# Proxy for executing functions to unsure error catching and proper timeouts
# returns the result of executing the function if it's successful or False to 
# indicate that something went wrong
# A Result is one of 
# False and the Execption if something went wrong 
# or
# Ret and None
# A Ret is any value or object return by performing the function call
# Function, List(any), ?Int ->  Result
def safe_execution(func, args = [], timeout = 3):
    ret = False
    exception = None

    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(func, *args)
            ret = future.result(timeout=timeout)
        except Exception as e:
            exception = e

    return ret, exception


def parse_json(input_bytes):
    decoder = json.JSONDecoder()

    elements = []
    position = 0

    while position != len(input_bytes):
        before_len = len(input_bytes[position:])
        after_len = len(input_bytes[position:].strip())
        if after_len == 0:
            break
        spaces_removed = before_len - after_len

        json_elem, json_len = decoder.raw_decode(input_bytes[position:].strip())

        position += (json_len + spaces_removed)
        elements.append(json_elem)
    return elements