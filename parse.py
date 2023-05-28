import pandas as pd

# Function to convert K and M to their numeric equivalents
def convert_k_m_to_numeric(value):
    if isinstance(value, str):
        value = value.replace(',', '')
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
    return float(value)

# Read the csv file
df = pd.read_csv('scraped_twitter_@0xkiichiro.csv')

# List of columns to parse
columns_to_parse = ['nu_of_comments', 'nu_of_likes', 'nu_of_retweets', 'tweet_impressions']

# Parse the columns
for column in columns_to_parse:
    df[column] = df[column].apply(convert_k_m_to_numeric)

# Save the parsed data back to csv
df.to_csv('parsed_file.csv', index=False)
