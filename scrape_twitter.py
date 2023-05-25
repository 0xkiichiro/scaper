from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import typer
from selenium.webdriver.common.keys import Keys
import csv

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

    with open(f'scraped_twitter_@{twitter_handle}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header first
        writer.writerow(['context', 'nu_of_comments', 'nu_of_likes', 'nu_of_retweets', 'tweet_impressions', 'owner_handle', 'owner_name', 'tweet_link', 'tweeted_at', 'created_at'])
        
        while True:
            try:
                # if notifications modal open, close it
                notifications_modal = driver.find_element(By.CSS_SELECTOR, '[data-testid="sheetDialog"]')
                clickable = notifications_modal.find_element(By.CSS_SELECTOR, '[role="button"]')
                clickable.click()
            except:
                pass

            owner_name = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]').text
            owner_handle = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/span').text
            tweets = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="tweet"]')
            last_height = driver.execute_script("return document.documentElement.scrollHeight")
            for tweet in tweets:
                tweet_link = tweet.find_element(By.XPATH, '//div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[3]/a').get_attribute('href')

                try:
                    context = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
                    tweeted_at = tweet.find_element(By.TAG_NAME, 'time').text
                    nu_of_comments = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="reply"]').text
                    nu_of_likes = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="like"]').text
                    nu_of_retweets = tweet.find_element(By.CSS_SELECTOR,'div[data-testid="retweet"]').text
                    # retweet = tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="socialContext"]')
                    # owner_name = retweet.find_element(By.XPATH, '//span').text
                except:
                    pass
                try:
                    tweet_impressions = tweet.find_element(By.XPATH, '//div/div/div[2]/div[2]/div[4]/div/div[4]/a/div/div[2]/span/span/span').text
                except:
                    tweet_impressions = 0
                ['context', 'nu_of_comments', 'nu_of_likes', 'nu_of_retweets', 'tweet_impressions', 'owner_handle', 'owner_name', 'tweet_link', 'tweeted_at', 'created_at']
                tweet_obj = [context, nu_of_comments, nu_of_likes, nu_of_retweets, tweet_impressions, owner_handle, owner_name, tweet_link, tweeted_at, str(time.localtime()[0]) + '.' + str(time.localtime()[1]) + '.' + str(time.localtime()[2])]
                if context not in context_list:
                    writer.writerow(tweet_obj)
                    context_list.append(context)
                    print(len(context_list),'->' , tweet_obj)

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

            # Export current data frame to csv
            if REACHED_PAGE_END:
                # df.to_csv(f'scraped_twitter_@{twitter_handle}.csv', index=False, encoding='utf-8')
                print('df exported to csv!')
                break

if __name__ == '__main__':
    app()