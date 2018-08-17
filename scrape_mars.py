import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Web scrape NASA Mars News site
    url = 'https://mars.nasa.gov/news/'
    
    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'lxml')

    news_title = soup.find('div', class_='content_title').a.text
    news_p = soup.find('div', class_='article_teaser_body').contents[0]

    # Web scrape JPL Mars Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'lxml')

    featured_image = soup.find('li', class_='slide').a['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_image}'

    # Web scrape Mars Weather twitter account
    url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(url)
    soup = BeautifulSoup(browser.html, 'lxml')

    tweets = soup.find_all('div', class_='js-tweet-text-container')

    # Find tweet with appropriate weather data
    mars_weather = ''
    criteria = ('Sol ', ', high ', ', low', ', pressure at')

    for tweet in tweets:
        if all(word in tweet.text for word in criteria):
            mars_weather = tweet.text.replace('\n','')
            break

    if mars_weather == '':
        mars_weather = 'No weather data is available at this time.'       

    # Web scrape Mars Facts Page
    url = 'https://space-facts.com/mars/'

    mars_table = pd.read_html(url)
    df = mars_table[0]
    df.columns = ['Description','Value']
    mars_facts_html = df.to_html(index=False)

    # Web scrape Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Create array of Mars Hemispheres
    hemispheres = ['Cerberus Hemisphere Enhanced',
                   'Schiaparelli Hemisphere Enhanced',
                   'Syrtis Major Hemisphere Enhanced',
                   'Valles Marineris Hemisphere Enhanced'
                  ]

    # Create array to store image dictionaries
    hemisphere_img_urls = []

    #Grab Mars Hemispheres
    for hemisphere in hemispheres:
        browser.visit(url)
        browser.click_link_by_partial_text(hemisphere)
        soup = BeautifulSoup(browser.html, 'lxml')
        img_url = soup.find('div', class_='downloads').a['href']
        hemisphere_img_urls.append({'title':hemisphere, 'img_url':img_url})

    # Close Browser
    browser.quit()

    # Create Mars Dictionary
    mars_dict = {'news':{'news_title':news_title, 'news_p':news_p},
                 'featured_image_url':featured_image_url,
                 'mars_weather':mars_weather,
                 'mars_facts_html':mars_facts_html,
                 'hemisphere_img_urls':hemisphere_img_urls
                }
    return mars_dict

