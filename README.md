RedditSentiment
Features
Terminal application that parses through the comments from top posts from a subreddit. Using Indico's Sentiment Analysis API, each image from its corresponding post is associated with a sentiment value. This sentiment value is then averaged across all the objects in the image which are classified using IBM Watson's Object Detection API. Each object is then given a moving sentiment over repeating objects from different posts and different comments. This data is then aggregated to suggest what objects to add to your own image to receive a more positive sentiment given similar background objects. Relevant data and findings are graphed using numpy and matplotlib.

Usage
Create virtual environment and run pip install. Change directories to local directory then run python main.py. Input the URL for what subreddit you want to analyze. When prompted enter the URL for your own image. Wait for results and you'll be provided with suggestions based on what else you can add to your image to receive more positive comments.

Comments
This was demoed at Hack Western where we won the sponsor award for the best use of Sentiment Analysis presented by Media Sonar. The demo was done using the Food subreddit and subsequently suggestions were given based on food sentiment. The data training was done over 200 reddit posts. Results can be viewed in the assets folder.
