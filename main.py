import praw

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
        file.write(str(submission) + "\n")
        print("title: ", submission.title)

        comments = submission.comments.list()
        for comment in comments:
            print(comment.body)
            file.write(comment.body + " " + "\n")

file.close()


