import pandas as pd

def convert_k_m_to_numeric(value):
    if isinstance(value, str):
        value = value.replace(',', '')
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
    return float(value)

df = pd.read_csv('scraped_twitter_@0xkiichiro.csv')

columns_to_parse = ['nu_of_comments', 'nu_of_likes', 'nu_of_retweets', 'tweet_impressions']

for column in columns_to_parse:
    df[column] = df[column].apply(convert_k_m_to_numeric)

df.to_csv('parsed_file.csv', index=False)
