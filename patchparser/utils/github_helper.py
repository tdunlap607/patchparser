"""
Helper functions to interact with GitHub
"""
import datetime
import time
import requests
import os

# LOAD the GitHub Token from an environment variable
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')


def github_rate_limit():
    """Obtains the remaining rate limit for your token

    Returns:
        json: Response of GitHub rate limit
    """
    headers = {'Authorization': 'token %s' % GITHUB_TOKEN}
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    response.close()
    return response.json()


def smart_limit(verbose=False):
    """
    Handles the GitHub rate limit issues
    """
    rate = github_rate_limit()
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