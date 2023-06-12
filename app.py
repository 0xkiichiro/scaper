from scrape_twitter import scrape
from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

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
        try:
            data = scrape(owner_handle)
            response = jsonify(data)
            return response
        except requests.exceptions.RequestException as e:
            return ex
    if request.method == 'GET':
        cursor = conn.execute(f'''
            SELECT * FROM scraped_tweets
            WHERE owner_handle == "@{owner_handle}"
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
            'quote_source_user': row[12],
            'quote_content': row[13],
            'owner_name': row[14],
            'is_quote': row[15],
            'has_media': row[16],
            'media_link': row[17]
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