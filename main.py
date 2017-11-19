import praw
import indicoio
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
import re
import time
import numpy as np
import matplotlib.pyplot as plt

indicoio.config.api_key = "150f3aff97a4936f8f0a8cd858345b9e"
reddit = praw.Reddit(client_id='L92JRMl9lgC4sA',
                     client_secret='fBQszj5hsjw0Ji3nk-UDo5sNZGo',
                     username='hackwestern4team',
                     password='RedditSentiment',
                     user_agent='RedditSentimentV1')

subreddit = reddit.subreddit('food')

hot_posts = subreddit.hot(limit=25)
submissionUrls = dict()

file = open("text.txt", "w")
submissions = list()
counter = 0
for submission in hot_posts:
    if not submission.stickied:
        print("Reading from: " + submission.url)
        submissionUrls[str(submission)] = submission.url
        submissions.append(str(submission))
        # print("title: ", submission.title)
        comments = submission.comments.list()
        counter = 0
        for comment in comments:
            counter += 1
            if counter > 4:
                break
            # print(comment.body)
            if hasattr(comment, 'body'):
                comment = (comment.body)
                comment = re.sub(r'[^\x00-\x7F]+', ' ', comment)
                file.write(((comment) + " " + "\n"))
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
    # print(linedict[submission])

# Reading the lines
sentimentComments = dict()
Scounter = 0
for submission in submissions:
    # reading the lines
    print("Finding sentiment value of " + submissionUrls[submission])
    multiLine = linedict[str(submission)]
    total = 0
    Scounter = Scounter + 1
    counter = 0
    for line in multiLine:
        if len(line) > 125:
            line = line[0:125]
        total = total + indicoio.sentiment_hq(line)
        counter = counter + 1
    if counter != 0:
        commentSentiment = total / counter
        sentimentComments[str(submission)] = commentSentiment
    else:
        sentimentComments[str(submission)] = 0.5

for key in sentimentComments:
    print(key, sentimentComments[key])

f.close()

objectSent = dict()
objectOccur = dict()
objectIDs = dict()
imageObjects = dict()
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='8d7aced8efa9ce11cca985d203dce5989cc20148')
for key in submissionUrls:
    hashmap = dict()
    listOfClasses = list()
    wholejson = (visual_recognition.classify(images_url=submissionUrls[key]))
    images = (json.dumps(wholejson['images'], indent=2)).splitlines()
    print("Identifying objects in " + submissionUrls[key])
    for line in images:
        if "\"class\":" in line:
            line = line.replace(",", "")
            line = line.replace("\"class\": \"", "")
            line = line.replace("\"", "")
            line = line.strip()
            listOfClasses.append(line)
            # print(line)
            if line in objectOccur:
                objectOccur[line] = objectOccur[line] + 1
                objectSent[line] = objectSent[line] + sentimentComments[key]
                objectIDs[line].append(key)
            else:
                if sentimentComments[key] > 0:
                    objectOccur[line] = 1
                    objectSent[line] = sentimentComments[key]
                    objectIDs[line] = list()
                    objectIDs[line].append(key)
    imageObjects[key] = listOfClasses

for key in objectSent:
    objectSent[key] = objectSent[key] / objectOccur[key]
    if objectOccur[key] > 2:
        print("key: ", key, objectSent[key])

# graph input x into x and y into y based on collected data
x = list()
y = list()

for key in objectSent:
    if objectOccur[key] > 2:
        x.append(key)
        y.append(objectSent[key])

x = x[:-1]
y = y[:-1]

newx = np.asarray(x)
newy = np.asarray(y)
height = newy
bars = newx
y_pos = np.arange(len(bars))
plt.barh(y_pos, height)
plt.yticks(y_pos, bars)
plt.show()

# Suggestion Area
while True:
    highestOfM = ""
    while highestOfM == "":
        print("Please enter image url:")
        marketingImageUrl = input()
        wholejson = (visual_recognition.classify(images_url=marketingImageUrl))
        images = (json.dumps(wholejson['images'], indent=2)).splitlines()
        listOfClasses = list()
        for line in images:
            if "\"class\":" in line:
                line = line.replace(",", "")
                line = line.replace("\"class\": \"", "")
                line = line.replace("\"", "")
                line = line.strip()
                listOfClasses.append(line)

        maxVal = 0
        appearedIn = list()
        highestOfM = ""
        for classs in listOfClasses:
            if classs in objectOccur:
                if objectSent[classs] > maxVal:
                    maxVal = objectSent[classs]
                    highestOfM = classs

    appearedIn = objectIDs[highestOfM]

    maxVal = 0
    highest = ""
    for key in appearedIn:
        if sentimentComments[key] > maxVal:
            maxVal = sentimentComments[key]
            highest = key

    print("\nYou should add:")
    for key in imageObjects[highest]:
        if objectSent[key] > objectSent[highestOfM] and objectSent[key]:
            print(key)
    print("\nYou should not add:")
    for key in imageObjects[highest]:
        if objectSent[key] <= objectSent[highestOfM]:
            print(key)
