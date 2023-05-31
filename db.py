import sqlite3

conn = sqlite3.connect('tweets.sqlite')

cursor = conn.cursor()
sql_query = '''CREATE TABLE scraped_tweets (
    id INTEGER PRIMARY KEY,
    context TEXT,
    nu_of_comments INTEGER NOT NULL,
    nu_of_likes INTEGER NOT NULL,
    nu_of_retweets INTEGER NOT NULL,
    tweet_impressions INTEGER NOT NULL,
    owner_handle TEXT NOT NULL,
    tweet_link TEXT NOT NULL,
    tweeted_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_retweet INTEGER NOT NULL,
    retweet_source_user TEXT,
    retweet_content TEXT,
    quote_source_key TEXT,
    quote_content TEXT,
    FOREIGN KEY (retweet_source_user) REFERENCES scraped_tweets(owner_handle)
)'''

cursor.execute(sql_query)