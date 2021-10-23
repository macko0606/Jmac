import praw
reddit = praw.Reddit(client_id = "DA4lc6KxY-dIXA", \
                            client_secret= "5TZEhmf6AdsXTHNgnjhJJGsEFmQ", \
                            user_agent= "Mimifur", \
                            username= "HereComesTheMoneyyy", \
                            password="EggSalami7")
hot_posts = reddit.subreddit("wallstreetbets").hot(limit=1)
for i in hot_posts:
    print(i.selftext)