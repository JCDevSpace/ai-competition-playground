from Game.Player.minimax_player import MinimaxPlayer
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pebble import ProcessPool, ThreadPool
import traceback
import json
import yaml


def generate_players(n, d):
    """Generates the specified number of MinimaxPlayer with the specified search depth of 2 for testing.

    Args:
        n (int): a positive integer
    """
    players = [None] * n

    for i in range(n):
        players[i] = MinimaxPlayer(str(i), i, depth=d)

    return players

def load_config(config_file):
    """Loads the configuration from the given yaml file and returns it as a dictionary of configurations.

    Args:
        config_file (str): a str of the yaml file

    Returns:
        dict: a dictionary of the configuration
    """
    config_dir = "../../../configs/"

    with open(config_dir + config_file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# def safe_execution(func, args=[], wait=False, timeout=None):
#     """Proxy function to execute function calls that might failed or require a timeout in case it takes too long, passes back the yeild from the executed function, else returns None when there are not return values or if an exception happenned while executing the given function.

#     Args:
#         func (func): a function to execute
#         args (list, optional): a list of argument to pass to the function when executing. Defaults to [].
#         wait (bool, optional): a boolean with true indicating to wait for the response from the executed function. Defaults to False.
#         timeout (int, optional): a positive interger that wait is set to true will wait for results from the executed function for the specified number of seconds. Defaults to None.

#     Returns:
#         tuple(x, exc): a tuple of the reture value from the executed function and the execption if one happen while executing 
#     """
#     ret = None

#     pool = ThreadPool()
#     try:
#         if not wait:
#             pool.schedule(func, args=args)
#             pool.close()
#             pool.join()
#         else:
#             future = pool.schedule(func, args=args)
#             pool.close()
#             pool.join(timeout=timeout)
#             ret = future.result()
#     except Exception:
#         print(traceback.format_exc())
#     return ret
from asyncio import get_event_loop, new_event_loop, set_event_loop, run, create_task, get_running_loop, ensure_future, sleep, run_coroutine_threadsafe


def safe_execution(func, args=[], wait=False, timeout=None):
    """Proxy function to execute function calls that might failed or require a timeout in case it takes too long, passes back the yeild from the executed function, else returns None when there are not return values or if an exception happenned while executing the given function.

    Args:
        func (func): a function to execute
        args (list, optional): a list of argument to pass to the function when executing. Defaults to [].
        wait (bool, optional): a boolean with true indicating to wait for the response from the executed function. Defaults to False.
        timeout (int, optional): a positive interger that wait is set to true will wait for results from the executed function for the specified number of seconds. Defaults to None.

    Returns:
        tuple(x, exc): a tuple of the reture value from the executed function and the execption if one happen while executing 
    """
    ret = None

    pool = ThreadPoolExecutor()
    try:
        if not wait:
            pool.submit(func, *args)
            pool.shutdown()
        else:
            loop = new_event_loop()
            coro = func(*args)
            future = pool.submit(run_async, coro, loop, timeout)
            loop.run_forever()
            ret = future.result()
            loop.close()
    except Exception:
        print(traceback.format_exc())
    return ret

def run_async(coro, loop, timeout):
    ret = None
    try:
        future = run_coroutine_threadsafe(coro, loop)
        ret = future.result(timeout=timeout)
    except TimeoutError:
        print("Timeout")
    except Exception:
        print(Exception)
    finally:
        loop.call_soon_threadsafe(loop.stop)
    return ret


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