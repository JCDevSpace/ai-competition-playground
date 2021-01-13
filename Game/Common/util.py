from Game.Player.minimax_player import MinimaxPlayer
from concurrent.futures import TimeoutError
from pebble import ProcessPool, ThreadPool

# from time import time, sleep

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

def safe_execution(func, args=[], wait=False, timeout=None):
    ret = None
    exception = None

    pool = ThreadPool()
    try:
        if not wait:
            pool.schedule(func, args=args)
            pool.close()
            pool.join()
        else:
            future = pool.schedule(func, args=args)
            pool.close()
            pool.join(timeout=timeout)
            ret = future.result()
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