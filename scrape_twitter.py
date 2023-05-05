from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import typer
from selenium.webdriver.common.keys import Keys

app = typer.Typer()


@app.command()
def scrape(twitter_handle: str):
    SCROLL_PAUSE_TIME = 2
    URL = f'https://twitter.com/{twitter_handle}'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    time.sleep(SCROLL_PAUSE_TIME)
    df = pd.DataFrame(columns=['context', 'nu_of_comments', 'nu_of_likes', 'views', 'owner_handle', 'owner_name', 'tweeted_at', 'created_at'])
    context_list = []
    REACHED_PAGE_END = False

    while True:
        owner_name = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]').text
        owner_handle = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/div/div/span').text
        tweets = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="tweet"]')

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        for tweet in tweets:
            action_group = driver.find_element(By.CSS_SELECTOR, '[role="group"]')
            context = tweet.find_element(By.XPATH, '//div/div/div[2]/div[2]/div[2]/div/span').text
            tweeted_at = tweet.find_element(By.TAG_NAME, 'time').text
            try:
                nu_of_comments = action_group.find_element(By.CSS_SELECTOR, f'[data-testid="reply"]').text
            except:
                nu_of_comments = 0
            try:
                likes = action_group.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
                nu_of_likes = likes.find_element(By.XPATH, '//div/div[2]/span/span/span').text
            except:
                nu_of_likes = 0

            tweet_obj = {
                'owner_name': owner_name,
                'owner_handle': owner_handle,
                'context': context,
                'nu_of_comments': nu_of_comments,
                'nu_of_likes': nu_of_likes,
                'tweeted_at': tweeted_at,
                'created_at': str(time.localtime()[0]) + '.' + str(time.localtime()[1]) + '.' + str(time.localtime()[2])
            }
            if context not in context_list:
                context_list.append(context)
                df = df._append(tweet_obj, ignore_index=True)
                print(tweet_obj)
                print('total length:', len(df), df.tail(1))


        # Scroll down to bottom
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        print('scroll down performed')
        print('new: ', new_height)

        # Check if we are end of the page
        if new_height == last_height:
            REACHED_PAGE_END = True
            print('reached to the end!')
        else:
            last_height = new_height
            print('keep going!')

        # Export current data frame to csv
        if REACHED_PAGE_END:
            df.to_csv(f'scraped_twitter_@{twitter_handle}.csv', index=False, encoding='utf-8')
            print('df exported to csv!')
            break

if __name__ == '__main__':
    app()