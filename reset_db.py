import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('tweets.sqlite')

# Create a cursor object
cursor = conn.cursor()

# Execute a query to delete all rows from the table
cursor.execute('DELETE FROM scraped_tweets')

# Commit the changes
conn.commit()

# Close the cursor and the database connection
cursor.close()
conn.close()
