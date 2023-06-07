from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import typer
from selenium.webdriver.common.keys import Keys
import sqlite3

app = typer.Typer()

@app.command()
def scrape(twitter_handle: str):
    SCROLL_PAUSE_TIME = 4
    URL = f'https://twitter.com/{twitter_handle}'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    print('waiting..')
    time.sleep(SCROLL_PAUSE_TIME)
    context_list = []
    REACHED_PAGE_END = False
    conn = sqlite3.connect('tweets.sqlite')
    cursor = conn.cursor()

    while True:
        try:
            # If notifications modal open, close it
            notifications_modal = driver.find_element(By.CSS_SELECTOR, '[data-testid="sheetDialog"]')
            clickable = notifications_modal.find_element(By.CSS_SELECTOR, '[role="button"]')
            clickable.click()
        except:
            pass

        current_time = time.localtime()
        formatted_time = f"{current_time.tm_year}.{current_time.tm_mon}.{current_time.tm_mday} {current_time.tm_hour}:{current_time.tm_min}"

        owner_name = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]').text
        owner_handle = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/span').text
        tweets = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="tweet"]')
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        pass_counter = 0

        for tweet in tweets:
            retweet_content = ''
            quote_source_key = ''
            quote_content = ''
            retweet_source_user = ''
            tweet_link = tweet.find_element(By.XPATH, './/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a').get_attribute('href')
            try:
                is_retweet = bool(tweet.find_element(By.CSS_SELECTOR, 'span[data-testid="socialContext"]').text)
                if is_retweet:
                    retweet_source_user = tweet.find_element(By.XPATH, './/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a/div/span').text
                    tweet_link = tweet.find_element(By.XPATH, './/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/div[2]/div/div[3]/a').get_attribute('href')
            except:
                is_retweet = False
            try:
                context = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
                tweeted_at = tweet.find_element(By.TAG_NAME, 'time').text
                nu_of_comments = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="reply"]').text
                nu_of_likes = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="like"]').text
                nu_of_retweets = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="retweet"]').text
            except:
                pass_counter+=1
                pass
            try:
                tweet_impressions = tweet.find_element(By.XPATH, './/div/div/div[2]/div[2]/div[4]/div/div[4]/a/div/div[2]/span/span/span').text
            except:
                tweet_impressions = 0

            # Create DB columns
            columns = ['context', 'nu_of_comments', 'nu_of_likes', 'nu_of_retweets', 'tweet_impressions', 'owner_handle', 'owner_name', 'tweet_link', 'tweeted_at', 'created_at', 'is_retweet', 'retweet_source_user', 'retweet_content','quote_source_key', 'quote_content']
            tweet_obj = [context, nu_of_comments, nu_of_likes, nu_of_retweets, tweet_impressions, owner_handle, owner_name, tweet_link, tweeted_at, formatted_time, is_retweet, retweet_source_user, retweet_content, quote_source_key, quote_content]

            if context not in context_list:
                cursor.execute(f'''
                    INSERT INTO scraped_tweets({', '.join(columns)}) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', tweet_obj)
                context_list.append(context)

        # Scroll down to bottom
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        # Wait to load page
        print('still waiting..')
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        print('scroll down performed')

        # Check if we are end of the page
        if new_height == last_height:
            REACHED_PAGE_END = True
            print('reached to the end!')
        else:
            last_height = new_height
            print('keep going!')

        # Write to DB
        if REACHED_PAGE_END:
            conn.commit()
            conn.close()
            print(f'scrape completed! {len(context_list)} tweets are scraped, number of passed tweets are {pass_counter}.')
            break

if __name__ == '__main__':
    app()