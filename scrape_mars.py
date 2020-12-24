# Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests
import pprint



##SET UP SCRAPE FUNCTION
def scrape():
    # Get everything going
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    #Establish the dictionary& functions
    mars_scrape_dict = {}
    news_results = nasa_mars_news_func(browser)
    mars_scrape_dict['nasa_title'] = news_results[0]
    mars_scrape_dict['nasa_paragraph']= news_results[1]
    mars_scrape_dict['featured_image_url']= jpl_mars_images_func(browser)
    mars_scrape_dict['facts_html']=mars_facts_func(browser)
    mars_scrape_dict['mars_urls']=mars_hemi_func(browser)
    return mars_scrape_dict

## NASA MARS NEWS
# Scrape Nasa Mars News Site & collect latest NEWS TITLE and PARAGRAPH TEXT

def nasa_mars_news_func(browser):   
    # Navigate chromebrowser window to NASA News site
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    # Set a manual delay.
    sleep(2) 
    # &run BeautifulSoup to parse the site's HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Get the latest headline
    nasa_title = soup.find_all("div", class_="content_title")[1].get_text()
    # Get the latest paragraph
    nasa_paragraph = soup.find_all("div", class_="article_teaser_body")[0].get_text()
    news_results = [nasa_title, nasa_paragraph]
    return news_results


##JPL MARS SPACE IMAGES
#Use splinter to find current FEATURED MARS IMAGE
# Open a new chrome browser window (and icon on task bar)
# uses chromedriver, not chrome

def jpl_mars_images_func(browser):
    # Navigate chromebrowser window to JPL images site
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    # Set a manual delay.
    sleep(2)
    # &run BeautifulSoup to parse the site's HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # USE SPLINTER to navigate & store jpg url:
    # Click on the FULL IMAGE link (in browser)
    browser.links.find_by_partial_text("FULL IMAGE").click()
    # Set a manual delay.
    sleep(2) 
    # Click on the MORE INFO link (in browser)
    browser.links.find_by_partial_text("more info").click()
    # Click on the JPEG image (in browser)
    browser.links.find_by_partial_text(".jpg").click()
    # Save a variable of the URL of the JPEG image file 
    featured_image_url = browser.url
    return featured_image_url

##Mars Facts!

# use pandas to scrape Mars Data table (facts and structure)
# include 9 items: Equatorial Diameter, Polar diameter, mass,
# moons, orbit , orbit, surface temp, first record, recorded by

def mars_facts_func(browser):
    # Define URL  (Mars Facts)
    facts_url = "https://space-facts.com/mars/"
    # Read in data table via Pandas. 
    # >> Specify [0] position to get just Mars data 
    facts_df = pd.read_html(facts_url)[0]
    # Create a polished dataframe with column headers and text clean-up
    facts_df.columns = ["Metric", "Planet Mars"]
    # Remove the colon character in DESCRIPTION column
    facts_df["Metric"] = facts_df["Metric"].str.replace(":","") 
    #display facts_df (for reference)
    facts_df
    # Use Pandas to convert the data to a HTML table string
    facts_df.set_index("Metric", inplace=True)
    # print(facts_html)
    facts_html = facts_df.to_html()
    #return something useable for html later
    return facts_html

## OVERVIEW: MARS HEMISPHERES
#  1. Visit USGS Astrogeology site & obtain hi res images for each of Mars' hemispheres
#  2. Click each link to open image url to full resolution
#  3. Save image url for full res image, and hemisphere tilte containing hemi. name. 
#   >> use a python dictionary to store the data using the keys "img_url" and "title"
#  4. Append the dictionary with the image url string and the hemisphere title to a list.
#     This list will contain one dictionary for each hemisphere

# MARS HEMISPHERES, step-by-step
#  Visit USGS Astrogeology site & obstain hi res images for each of Mars' hemispheres

def mars_hemi_func(browser):
# Navigate chromebrowser window to MARS HEMISPHERES website    
    mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_url)
    # Set a manual delay.
    sleep(2) 
    # &run BeautifulSoup to parse the site's HTML
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Create dictionary for URLs & pics (empty); Create list for image URLs (empty); 
    # Create list of hemisphere names (FILLED)
    mars_dict = {}
    mars_hemi_urls = []
    mars_hemi = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]
    # Loop through hemispheres by name, populate dictionary with URL and pic
    for hemi in mars_hemi:
        print(hemi)
        sleep(3)
        browser.links.find_by_partial_text(hemi).click()

        face_html = browser.html
        soup = BeautifulSoup(face_html, "html.parser")
        
        mars_dict["title"]= soup.find("h2").get_text().replace("Enhanced","").strip()
        mars_dict["img_url"] = soup.find_all("div", class_="downloads")[0].find_all("a")[0]["href"]
        mars_hemi_urls.append(mars_dict) 

    # go back to main directory
        browser.back()

    # print(mars_hemi_urls)
    return mars_hemi_urls

if __name__ == "__main__":
    scrape()
# STEP 2: ON TO MONGO DB & FLASK.....
                  
