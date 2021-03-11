from src.player.minimax_player import MinimaxPlayer
from asyncio import wait_for
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
    config_dir = "/home/jing/ai-competition-playground/configs/"

    with open(config_dir + config_file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)

async def safe_async_exec(func, args=[], returns=False, timeout=None):
    """Safely execute the given coroutine with the given arguments with the given return and timeout configurations, returns None if there was a problem during execution or timed out.

    Args:
        func (coroutine): a coroutine to execute
        args (list, optional): a list of arguments to pass the coroutine when executing. Defaults to [].
        returns (bool, optional): a boolean with True indicating returning the yeild from the coroutine to caller. Defaults to False.
        timeout (int, optional): a non negative integer indicating how long to wait before returning control to caller. Defaults to None.

    Returns:
        union(x, None): the yield form the coroutine or None
    """
    ret = None
    try:
        if not returns:
            await wait_for(func(*args), timeout)
        else:
            ret = await wait_for(func(*args), timeout)
    except Exception:
        pass

    return ret