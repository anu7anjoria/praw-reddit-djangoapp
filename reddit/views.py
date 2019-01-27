from django.shortcuts import render
from django.http import HttpResponse
import praw
import requests
from .models import Post
DisplaySubmission = []

#   def index(request):
  #  return HttpResponse("<h1>page here</h1>")

def parm(request,slug):
    reddit = praw.Reddit(client_id='5djWuT7lVQZwUA',
                      client_secret='7HqoHyGoRo8ZHJq3ZBp2jTQtb9U',
                      user_agent='thisisnotneeded')    

    subreddit = reddit.subreddit(slug)
    for submission in subreddit.hot(limit=10):
        DisplaySubmission.append(submission)


    context = {'DisplaySubmission':DisplaySubmission}
    return render(request,'reddit/index.html',context)