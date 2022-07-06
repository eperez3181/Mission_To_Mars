# Automates browser actions
from splinter import Browser

# Parses the HTML
from bs4 import BeautifulSoup
import pandas as pd
import time

# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
#def scrape():
    # Setup splinter
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
    # Set an empty dict for listings that we can save to Mongo
def scrape():
    browser =init_browser()
    NASA_mars_news = {}

    # Mars News info: url to scrap
    url = "https://redplanetscience.com/"
    # Call visit on our browser and pass in the URL we want to scrape   
    browser.visit(url)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html

    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = BeautifulSoup(html, "html.parser")

    # Build our dictionary for the headline, price, and neighborhood from our scraped data
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    NASA_mars_news["title"] = news_title
    NASA_mars_news["paragraph"]= news_p


    # Scrap Mars featured image
    url2 = 'https://spaceimages-mars.com/'
    browser.visit(url2)
    time.sleep(1)
    html2 = browser.html
    soup = BeautifulSoup(html2, 'html.parser')
    featured_relative_path = soup.find_all('img')[1]["src"]
    featured_image_url = url2 + featured_relative_path
    NASA_mars_news["img"]= featured_image_url


    # Scrap Mars facts
    url3 = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url3)
    df= tables[0]
    df = df.rename(columns ={0: "Description",
                        1: "Mars",
                        2: "Earth"})
    
    df.set_index("Description", inplace=True)
    
    html_table = df.to_html()
    html_table.replace('\n', '').replace("text-align: right;", "text-align: left;")
    NASA_mars_news["table"] = html_table.replace('\n', '').replace("text-align: right;", "text-align: left;")


    # Scrap Mars Hemispheres
    url4 = 'https://marshemispheres.com'
    browser.visit(url4)
    time.sleep(1)
    html4 = browser.html
    soup = BeautifulSoup(html4, 'html.parser')  
    hemispheres = soup.find_all("div", class_="item")

    href = []
    for hemisphere in hemispheres:
        href.append(url4 +"/"+(hemisphere.find("a", class_="itemLink product-item")["href"]))
    
    hemisphere_image_urls = []
    for url in href:
        browser.visit(url)
        time.sleep(1)
        html5=browser.html
        soup=BeautifulSoup(html5, 'html.parser')
        title = soup.find("h2", class_="title").text
        img_url = url4 +"/"+ soup.find("img", class_="wide-image")["src"]
        hemisphere_image_urls.append({"title":title, "img_url":img_url})
        time.sleep(1)
    NASA_mars_news["hemisphere"]=hemisphere_image_urls


    # Quit the browser
    browser.quit()

    # Return our dictionary
    return NASA_mars_news

