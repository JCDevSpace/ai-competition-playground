from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import TimeoutError

import json

def safe_execution(func, args=[], wait=False, timeout=None):
    ret = None
    exception = None

    with ThreadPoolExecutor() as executor:
        try:
            future = executor.submit(func, *args)
            if wait:
                if timeout:
                    from time import time
                    print("start waiting")
                    start = time()
                    ret = future.result(timeout=timeout)
                    print("finished waiting in", time() - start, "seconds")
                else:
                    print("start waiting indefinately")
                    ret = future.result()
        except Exception as e:
            if isinstance(e, TimeoutError):
                print("timed out in", time()-start, "seconds")
            else:
                print(e)
            exception = e

        executor.shutdown(wait=False)
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