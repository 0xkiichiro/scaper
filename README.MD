# Youtube Scraper

This tool allows you to scrape your preferred youtube videos & tweets

## Usage

To use download this repository to your local, create a venv, install the requirements

`pip install -r requirements.txt`

& simply type the following command into your terminal:

Youtube: `python scrape_youtube.py <channel_name>`

Twitter: `python scrape_twitter.py <twitter_handle>`

Here's an example command for scraping Joe Rogan's videos:

Youtube: `python scrape_youtube.py joerogan`

Twitter: `python scrape_twitter.py joerogan`

There is an example CSV file in the repository that you can preview to see which attributes we are scraping.

Currently, we support scraping the following attributes:

### Youtube

- Video name
- Video views
- Video link
- Video creation date
- Video scraping date

### Twitter

- owner name
- owner handle
- tweet context
- number of comments
- number of likes
- number of rewtweets
- number of impressions
- tweet link
- tweeted at

## Code

The code for this tool uses the following libraries:

- selenium
- pandas
- time
- typer

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import typer

app = typer.Typer()


@app.command()
def scrape(channel_name: str):
    URL = f'https://www.youtube.com/@{channel_name}/videos'
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    df = pd.DataFrame(columns=['title', 'views', 'when', 'link', 'created_at'])
    titles = []
    REACHED_PAGE_END = False
    SCROLL_PAUSE_TIME = 1

    while True:
        videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-grid-media')
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        print('old: ', last_height)

        for video in videos:
            title = video.find_element(By.ID, 'video-title').text
            metadata = video.find_elements(By.CLASS_NAME, 'inline-metadata-item')
            link = video.find_element(By.ID, 'thumbnail').get_attribute('href')

            video_obj = {
                'title':title,
                'views': metadata[0].text,
                'when': metadata[1].text,
                'link': link,
                'created_at': str(time.localtime()[0]) + '.' + str(time.localtime()[1]) + '.' + str(time.localtime()[2])
            }

            if title not in titles:
                titles.append(title)
                df = df._append(video_obj, ignore_index=True)
                print('total length:', len(df), df.tail(1))


        # Scroll down to bottom
        driver.execute_script("document.body.scrollTop = document.body.scrollHeight;")
        driver.execute_script("document.documentElement.scrollTop = document.documentElement.scrollHeight;")

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
            df.to_csv(f'scraped_youtube_@{channel_name}.csv', index=False, encoding='utf-8')
            print('df exported to csv!')
            break

if __name__ == '__main__':
    app()
```

## Conclusion

Happy scraping!

You can reach me for any questions & feature requests on:

Github: https://github.com/0xkiichiro |
Twitter: https://twitter.com/0xkiichiro

## License

This tool is released under the MIT License.
