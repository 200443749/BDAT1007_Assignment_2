import tweepy
from flask import Flask, render_template, session, request, redirect
from flask import Flask, jsonify, render_template, url_for
from flask.templating import render_template_string
from pymongo import MongoClient
from bson import ObjectId
import os
import pandas as pd
import csv
import requests
import praw,json,datetime

app = Flask(__name__)

# connection with MongoDB
client = MongoClient("mongodb+srv://binay_99:Watson%4099@bdat1007.n5kgy.mongodb.net/test?authSource=admin&replicaSet=atlas-124cba-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db=client["Data_Mining_db"]
mytweet=db["TweetPost"]
myreddit=db["RedditPost"]

# connection with MongoDB

# Index
@app.route("/")
def index():
    tweet_list=mytweet.find().sort([("PostDate",-1)])
    reddit_list=myreddit.find().sort([("PostDate",-1)])
    return render_template('index.html',tweet_list=tweet_list,reddit_list=reddit_list)

# Twitter

# Consumer keys and access tokens, used for OAuth
consumer_key = '6YzIHNpaOYfN0MJa5mTG5tKML'
consumer_secret = 'MwDGrW7LGx0x4F9qhWJskAPGRDop9iySsVkKXiSkZu8A4s1pf3'
access_token = '1301043779638419456-L92GZNvHc5or1pWTQUvELIsA3x2JIo'
access_token_secret = 'f2E6Izk6kmobBGGX1O7xHz09muRP0qKPwrfA7yOA3kOcK'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Twitter
@app.route("/Twitterform")
def twitterform():
    posted=False;
    return render_template('Twitterform.html')

@app.route("/Twitterform",methods=['POST','GET'])
def Twitterform():
    if request.method == 'POST':
       Tweet= request.form['Tweetpost']
       api.update_status(Tweet)
       name="Binay_999"
       now = datetime.datetime.now()
       mydict = {"Tweet":Tweet,"PostDate":now,"Name":name}
       message=''
       try:
           mytweet.insert_one(mydict)
           posted=True
           message="Tweet successfully!"
       except:
            message="Something else gone wrong!!"
            return message
       guitar_list=mytweet.find()
       return render_template('Twitterform.html',message=message)
# Twitter


#Reddit
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

# Reddit
@app.route("/Redditform")
def redditform():
    posted=False;
    return render_template('Redditform.html')

@app.route("/Redditform",methods=['POST','GET'])
def Redditform():
    if request.method == 'POST':
       reddit_title= request.form['title']
       reddit_description= request.form['description']
       myredditdict = {"Title":reddit_title,"Description":reddit_description}
       title = reddit_title
       selftext = reddit_description
       subreddit.submit(title,selftext=selftext)
       name="Binay_99"
       now = datetime.datetime.now()
       mydict = {"Title":reddit_title,"Description":reddit_description,"PostDate":now,"Name":name}
       message=''
       try:
           myreddit.insert_one(mydict)
           posted=True
           message="Information posted successfully!"
       except:
            message="Something else gone wrong!!"
            return message
       return render_template('Redditform.html',message=message)
# Reddit

if __name__ == "__main__":
    app.run(debug=True)