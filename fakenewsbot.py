import praw
# PRAW = Python Reddit API Wrapper
import re
from time import sleep
import random
from random import randint

r = praw.Reddit('botname')  # we use r to call Praw and access Reddit API data
subreddit = r.subreddit("Test")  # choosing the subreddit our bot should operate in


submission_response = ['SubmissionResponse1','SubmissionResponse2']
reply_response = ['ReplyResponse1','ReplyResponse2']

count_iter = 1  # runtime variable

while True:
    f = open('IDs_responded_to.txt', 'a+')  # open a textfile to store submission IDs
    f.seek(0)
    SIDs = f.readlines()  # creates a list of the IDs saved in our textfile

    for submission in subreddit.new(limit=5):   # scans the newest posts in the subreddit, limited to 5
        if str(submission.id) + '\n' not in SIDs:  # checking, if our bot already replied to the submissions
            if re.search("TestWord", submission.title, re.IGNORECASE) and submission.author != r.user.me():
                # here we can specify the expression which should be in the post title
                submission.reply(random.choice(submission_response))    # random choice of our pool of answers for submissions
                print("Bot replying to : ", submission.title)   # console output
                f.write(submission.id + '\n')   # adding the submission ID to our textfile
    f.close()

    f = open('comments_replied_to.txt', 'a+')
    f.seek(0)
    CIDs = f.readlines()

    for comment in subreddit.comments(limit=5):  # same structure as above, but for comments
        if str(comment.id) + '\n' not in CIDs:
            if re.search("TestWord", comment.body, re.IGNORECASE) and comment.author != r.user.me():
                comment.reply(random.choice(reply_response))
                print("Bot replying to : ", comment.body)
                f.write(comment.id + "\n")

        sleep(randint(1, 3))   # one possible option to make our bot more human like

        for i in r.inbox.unread(limit=5):   # checking if someone answered out comments, and then replying to them
            if str(comment.id) + '\n' not in CIDs and comment.author != r.user.me():  # only replying, if we haven't already in "comments"
                comment.reply(random.choice(reply_response))
                print("Bot replying to : ", comment.body)
                f.write(comment.id + "\n")
                i.mark_read()
    f.close()

    print("Iteration %d complete." % count_iter)

    count_iter += 1

    print("Iteration %d begins." % count_iter)

    sleep(randint(3, 7))  #  wait time before new cycle


