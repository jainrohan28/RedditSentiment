import praw
import indicoio
import json
import matplotlib.pyplot as plt
import numpy as np
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

indicoio.config.api_key = "1b8cc780f7b973494eac71a19a6a917a"

reddit = praw.Reddit(client_id='L92JRMl9lgC4sA',
                     client_secret='fBQszj5hsjw0Ji3nk-UDo5sNZGo',
                     username='hackwestern4team',
                     password='RedditSentiment',
                     user_agent='RedditSentimentV1')

subreddit = reddit.subreddit('pics')

hot_posts = subreddit.hot(limit=3)
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
        if len(line) > 256:
            line = line[0:255]
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
objectIDs = dict()
imageObjects = dict()
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
                objectIDs[line].append(key)
                print("Add sentiment value to "+line+" of "+str(objectSent[line]))
            else:
                objectOccur[line] = 1
                objectSent[line] = sentimentComments[key]
                objectIDs[line] = list()
                objectIDs[line].append(key)
                print("First Time: Add sentiment value to " + line + " of " + str(objectSent[line]))
    imageObjects[key] = listOfClasses

for key in objectSent:
    if objectOccur[key] > 0:
        print("key: ", key, objectSent[key]/objectOccur[key])

# graph input x into x and y into y based on collected data
x = ('1', '2', '3')
y = (1000, 2000, 3000)
y_pos = np.arange(len(x))

plt.bar(y_pos, y)
plt.show()

# Suggestion Area
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

maxVal=0
appearedIn = list()
highest = ""
for classs in listOfClasses:
    if classs in objectOccur:
        if objectSent[classs] > maxVal:
            maxVal = objectSent[classs]
            highest = classs

appearedIn = objectIDs[highest]

maxVal = 0
highest = ""
for key in appearedIn:
    if sentimentComments[key] > maxVal:
        maxVal = sentimentComments[key]
        highest = key

for key in imageObjects[highest]:
    print("You should add " + key)
