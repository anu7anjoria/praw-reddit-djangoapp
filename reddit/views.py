
from django.shortcuts import render
from django.http import HttpResponse
import praw
import re
import time
import requests
import random
from .models import Post
common_spammy_words = []
spam_words = []
DisplaySubmission = []

reddit = praw.Reddit(client_id='7O0YOVKSIT7aTg',
                     client_secret='akj2gzdK49pbLimu-CDM8-CsQUs',
                     user_agent='noneed') 
def find_spam_by_name(search_query):
    authors = []
    for submission in reddit.subreddit("all").search(search_query, sort="new", limit=11):
        print(submission.title, submission.author, submission.url)
        if submission.author not in authors:
            authors.append(submission.author)
    print(20*'-')
    print(authors)
    print(20*'-')
    return authors

def parm(request,slug):
    subreddit = reddit.subreddit(slug)

 #   for submission in subreddit.hot(limit=100   ):
 #       DisplaySubmission.append(submission)
    find_spam_by_name(slug)
    context = {'DisplaySubmission':DisplaySubmission}
    return render(request,'reddit/index.html',context)

if __name__ == "__main__":
    # Compile regex from spam_words.txt for checking titles
    print(20*'!')
    with open("spam_words.txt") as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            try:
                common_spammy_words.append(re.compile(line))
            except:
                print(20*'-')
                print(f"Failed to compile {line}")
                continue

    while True:
        current_search_query = random.choice(["udemy"])
        spam_content = []
        trashy_users = {}
        smelly_authors = find_spam_by_name(current_search_query)
        for author in smelly_authors:
            user_trashy_urls = []
            sub_count = 0
            dirty_count = 0
            try:
                for sub in reddit.redditor(str(author)).submissions.new():
                    submit_links_to = sub.url
                    submit_id = sub.id 
                    submit_subreddit = sub.subreddit
                    submit_title = sub.title
                    dirty = False
                    for regex in common_spammy_words:
                        if re.search(regex, submit_title.lower()):
                            dirty = True
                            junk = [submit_id,submit_title]
                            if junk not in user_trashy_urls:
                                user_trashy_urls.append([submit_id,submit_title,str(author)])

                    if dirty:
                        dirty_count += 1
                    sub_count += 1

                try:
                    trashy_score = dirty_count/sub_count
                except: trashy_score = 0.0
                print("User {} trashy score is: {}".format(str(author), round(trashy_score,3)))

                if trashy_score >= 0.5 and sub_count > 1:
                    trashy_users[str(author)] = [trashy_score,sub_count]

                    for trash in user_trashy_urls:
                        spam_content.append(trash)  

            except Exception as e:
                print(str(e))

        for spam in spam_content:
            spam_id = spam[0]
            spam_user = spam[2]
            submission = reddit.submission(id=spam[0])
            created_time = submission.created_utc
            tagged = False

            for comment in submission.comments.list():
                comment_text = comment.body
                if "*Beep boop*" in comment_text:
                    print("This submission has already been tagged.")
                    tagged = True