import praw
import indicoio
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

indicoio.config.api_key = "f42c71470b2fb82f25ebfd66215c0215"

reddit = praw.Reddit(client_id='L92JRMl9lgC4sA',
                     client_secret='fBQszj5hsjw0Ji3nk-UDo5sNZGo',
                     username='hackwestern4team',
                     password='RedditSentiment',
                     user_agent='RedditSentimentV1')

subreddit = reddit.subreddit('pics')

hot_posts = subreddit.hot(limit=1)
submissionUrls = dict()

file = open("text.txt", "w")
submissions = list()
for submission in hot_posts:
    if not submission.stickied:
        print(submission.url)
        submissionUrls[str(submission)] = submission.url
        submissions.append(str(submission))
        # print("title: ", submission.title)
        comments = submission.comments.list()
        counter = 0
        for comment in comments:
            counter += 1
            if counter > 29:
                break
            # print(comment.body)
            if hasattr(comment, 'body'):
                file.write(comment.body + " " + "\n")
        file.write(str(submission))
        file.write("\n")

file.close()

# open read file
f = open("text.txt", "r")
linedict = dict()

for submission in submissions:
    lines = list()
    for line in f:
        line = (line.rstrip())  # for line in f_in)
        if line == submission:
            break
        if line != "":
            lines.append(line)  # list(line #for line in lines if line)
    linedict[submission] = lines
    print(linedict[submission])

#Reading the lines
sentimentComments = dict()
for submission in submissions:
    #reading the lines
    multiLine = linedict[str(submission)]
    total = 0
    counter = 0
    for line in multiLine:
        total = total + indicoio.sentiment_hq(line)
        counter = counter + 1
    if counter != 0:
        commentSentiment = total/counter
        sentimentComments[str(submission)] = commentSentiment
    else:
        sentimentComments[str(submission)] = 0

for key in sentimentComments:
    print(key, sentimentComments[key])

f.close()

objectSent = dict()
objectOccur = dict()
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='ccc5c78d342ad2426470bfe29416b8bdc7e655e5')
for key in submissionUrls:
    hashmap = dict()
    listOfClasses = list()
    print(submissionUrls[key])
    wholejson = (visual_recognition.classify(images_url=submissionUrls[key]))
    print(wholejson)
    images = (json.dumps(wholejson['images'], indent=2)).splitlines()

    for line in images:
        if "\"class\":" in line:
            line = line.replace(",","")
            line = line.replace("\"class\": \"", "")
            line = line.replace("\"", "")
            line = line.strip()
            listOfClasses.append(line)
            #print(line)
            if line in objectOccur:
                objectOccur[line] = objectOccur[line] + 1
                objectSent[line] = objectSent[line] + sentimentComments[key]
                print("Add sentiment value to "+line+" of "+str(objectSent[line]))
            else:
                objectOccur[line] = 1
                objectSent[line] = sentimentComments[key]
                print("First Time: Add sentiment value to " + line + " of " + str(objectSent[line]))

for key in objectSent:
    if objectOccur[key] > 5:
        print(key, objectSent[key]/objectOccur[key])