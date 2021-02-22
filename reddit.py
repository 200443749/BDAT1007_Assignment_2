import json
import praw
import requests

subr = 'pythonsandlot'
credentials = 'client_secrets.json'
with open(credentials) as f:
    creds = json.load(f)
reddit = praw.Reddit(client_id=creds['client_id'],
                     client_secret=creds['client_secret'],
                     user_agent=creds['user_agent'],
                     redirect_uri=creds['redirect_uri'],
                     refresh_token=creds['refresh_token'])
subreddit = reddit.subreddit(subr)
title = 'This is my first attempt in reddit'
selftext = '''
ascjnsdjkcn
'''
subreddit.submit(title,selftext=selftext)
