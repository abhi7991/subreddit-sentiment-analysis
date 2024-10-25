# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 15:37:39 2024

@author: abhis
"""


import scrapy
from scrapy import Selector

import pandas as pd
from pandas.io import sql
import time

import os
import requests
import json
from bs4 import BeautifulSoup

import re
import ast
import datetime as datetime
from pytz import timezone
import requests, zipfile, io
import csv
import numpy as np

import praw

from dotenv import load_dotenv
load_dotenv(override=True)
#%%
# Set up your Reddit app credentials
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='movieSentiment',  # Can be any string, usually your app name or your Reddit username
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

# Access the subreddit 'r/movies'
subreddit = reddit.subreddit('moviecritic')
# Search for posts containing "Jurassic Park" in the r/movies subreddit
query = 'Jurassic Park'
results = subreddit.search(query,sort='top' ,limit=10)

# Function to extract comments recursively
def get_comments(submission):
    submission.comments.replace_more(limit=0)  # Replaces "MoreComments" objects
    comments = []
    for comment in submission.comments.list():
        comments.append(comment.body)
    return comments

# Create a dictionary to store posts and their comments
posts_data = []

# Loop through the results and store posts and their comments
for submission in results:
    post_info = {
        "title": submission.title,
        "score": submission.score,
        "author": str(submission.author),
        "url": submission.url,
        "body": submission.selftext,
        "comments": get_comments(submission)
    }
    posts_data.append(post_info)

# Print the dictionary or store it as needed
for post in posts_data:
    print(post)

#%%
import praw

# Access the subreddit 'r/movies'
subreddit = reddit.subreddit('movies')

# Refine your query to focus on thoughts and opinions about Jurassic Park
query = 'Jurassic Park thoughts OR opinions OR review OR discussion'

# Search for relevant posts, sort by top posts, and search from all time
results = subreddit.search(query, sort='top', time_filter='all', limit=10)

# Store posts and comments in a dictionary
posts_data = []

def get_comments(submission):
    submission.comments.replace_more(limit=0)
    return [comment.body for comment in submission.comments.list()]

for submission in results:
    post_info = {
        "title": submission.title,
        "score": submission.score,
        "author": str(submission.author),
        "url": submission.url,
        "body": submission.selftext,
        "comments": get_comments(submission)
    }
    posts_data.append(post_info)

# Print or save the data
for post in posts_data:
    print(post)

#%%
import praw
from fpdf import FPDF  # fpdf2 should work similarly with FPDF

# Access the subreddit 'r/movies'
subreddit = reddit.subreddit('movies')

# Refine your query to focus on thoughts and opinions about Jurassic Park
query = 'Jurassic Park thoughts OR opinions OR review OR discussion'

# Search for relevant posts, sort by top posts, and search from all time
results = subreddit.search(query, sort='top', time_filter='all', limit=10)

# Function to extract comments recursively
def get_comments(submission):
    submission.comments.replace_more(limit=0)  # Replaces "MoreComments" objects
    comments = []
    for comment in submission.comments.list():
        comments.append(comment.body)
    return comments

# Open a text file to write the output
with open("jurassic_park_reddit_discussion.txt", "w", encoding="utf-8") as file:
    for submission in results:
        # Write post details to the text file
        file.write(f"Post Title: {submission.title}\n")
        file.write(f"Author: {submission.author}\n")
        file.write(f"Score: {submission.score}\n")
        file.write(f"Content:\n{submission.selftext}\n")
        file.write("\n" + "-"*50 + "\n")  # Separator line


        # Write comments to the text file
        comments = get_comments(submission)
        file.write("Comments:\n")
        
        for comment in comments:
            file.write(f"- {comment}\n")
        
        # Add a separator line between posts
        file.write("\n" + "="*50 + "\n")  # Another separator for clarity

print("Text file created successfully.")