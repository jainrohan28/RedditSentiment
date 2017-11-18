import praw
import indicoio

reddit = praw.Reddit(client_id='L92JRMl9lgC4sA',
                     client_secret='fBQszj5hsjw0Ji3nk-UDo5sNZGo',
                     username='hackwestern4team',
                     password='RedditSentiment',
                     user_agent='RedditSentimentV1')

subreddit = reddit.subreddit('eyebleach')

hot_eyebleach = subreddit.hot(limit=4)

file = open("text.txt", "w")
for submission in hot_eyebleach:
    if not submission.stickied:
        print(submission.url)
        file.write(str(submission) + "\n")
        # print("title: ", submission.title)

        comments = submission.comments.list()
        for comment in comments:
            # print(comment.body)
            file.write(comment.body + " " + "\n")

file.close()

counter = 0
total = 0

indicoio.config.api_key = "f42c71470b2fb82f25ebfd66215c0215"

#Open the read file
f = open("text.txt", "r")
lines = list()

for line in f:
    line = (line.rstrip()) #for line in f_in)
    if line != "":
        lines.append(line)                #list(line #for line in lines if line)
#Reading the lines
for line in lines:
    #reading the lines
    singleLine = line
    total = total + indicoio.sentiment_hq(singleLine)
    #increase counter
    counter = counter + 1

print("total:", total)
print(counter)
print(total / counter)


