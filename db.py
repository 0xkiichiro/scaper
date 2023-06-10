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
    quote_source_user TEXT,
    quote_content TEXT,
    owner_name TEXT,
    is_quote INTEGER NOT NULL,
    has_media INTEGER NOT NULL,
    media_link TEXT
)'''

cursor.execute(sql_query)

conn.commit()
conn.close()