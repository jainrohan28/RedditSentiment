import praw
import indicoio

indicoio.config.api_key = "f42c71470b2fb82f25ebfd66215c0215"

reddit = praw.Reddit(client_id='L92JRMl9lgC4sA',
                     client_secret='fBQszj5hsjw0Ji3nk-UDo5sNZGo',
                     username='hackwestern4team',
                     password='RedditSentiment',
                     user_agent='RedditSentimentV1')

subreddit = reddit.subreddit('screensavers')

hot_eyebleach = subreddit.hot(limit=4)

file = open("text.txt", "w")
submissions = list()
for submission in hot_eyebleach:
    if not submission.stickied:
        print(submission.url)
        submissions.append(str(submission))
        # print("title: ", submission.title)
        comments = submission.comments.list()
        for comment in comments:
            # print(comment.body)
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
