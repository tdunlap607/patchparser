"""
Helper functions to interact with GitHub
"""
import datetime
import time
import requests


def github_rate_limit(token: str):
    """Obtains the remaining rate limit for your token

    Args:
        token (str): API Token

    Returns:
        json: Response of GitHub rate limit
    """
    headers = {'Authorization': 'Bearer %s' % token}
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    response.close()
    return response.json()


def smart_limit(token: str, verbose=False):
    """
    Handles the rate limit issues

    Args:
        token (str): API Token

    Returns:
        json: Response of GitHub rate limit
    """
    rate = github_rate_limit(token=token)
    rate_limit_remaining = rate['rate']['remaining']
    reset = datetime.datetime.fromtimestamp(rate["rate"]["reset"])
    if verbose:
        print(f"Rate Limit Remaining: {rate_limit_remaining} | "
              f"Reset: {reset} | "
              f"Current time: {datetime.datetime.now()}")

    """Handles rate limit issues"""
    if rate_limit_remaining <= 50:
        """Get seconds until reset occurs"""
        time_until_reset = reset - datetime.datetime.now()
        print(f"Seconds until reset: {time_until_reset.seconds}")
        print(f"Starting sleep countdown now: {datetime.datetime.now()}")
        """Sleep until rate limit reset...add 30 seconds to be safe"""
        for i in reversed(range(0, time_until_reset.seconds, 60)):
            print(f"Sleep state remaining: {i} seconds.")
            time.sleep(60)
