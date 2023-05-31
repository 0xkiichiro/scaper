from scrape_twitter import scrape
from flask import Flask, request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)
obj = {'hello': 'world'}

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('tweets.sqlite')
    except sqlite3.Error as e:
        print(e)
    return conn

@app.route('/tweets/<owner_handle>', methods=['GET', 'POST'])
def scrape_tweets(owner_handle):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        response = jsonify(obj)
        return response
    
    if request.method == 'GET':
        cursor = conn.execute(f'''
            SELECT * FROM scraped_tweets
            WHERE owner_handle == "{owner_handle}"
        ''')
        
        tweets = [
        {
            'id': row[0],
            'context': row[1],
            'nu_of_comments': row[2],
            'nu_of_likes': row[3],
            'nu_of_retweets': row[4],
            'tweet_impressions': row[5],
            'owner_handle': row[6],
            'tweet_link': row[7],
            'tweeted_at': row[8],
            'created_at': row[9],
            'is_retweet': bool(row[10]),
            'retweet_source_user': row[11],
            'retweet_content': row[12],
            'quote_source_key': row[13],
            'quote_content': row[14]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    if tweets:
        return jsonify(tweets)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run()