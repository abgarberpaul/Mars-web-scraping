#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests
import pprint


# In[2]:


## NASA MARS NEWS
# scrape Nasa Mars News Site & collect latest NEWS TITLE and PARAGRAPH TEXT


# In[3]:


# Open a new chrome browser window (and icon on task bar)
# uses chromedriver, not chrome

executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[26]:


# Navigate chromebrowser window to NASA News site
nasa_url = "https://mars.nasa.gov/news/"
browser.visit(nasa_url)

# Set a manual delay.
sleep(3) 

# &run BeautifulSoup to parse the site's HTML
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[27]:


nasa_title = soup.find_all("div", class_="content_title")[1].get_text()
nasa_title


# In[29]:


# Grab the latest paragraph
nasa_title = soup.find_all("div", class_="article_teaser_body")[0].get_text()
nasa_title


# In[6]:


# Close the chromebrowser window
browser.quit()


# In[7]:


##JPL MARS SPACE IMAGES
#Use splinter to find current FEATURED MARS IMAGE


# In[8]:


# Open a new chrome browser window (and icon on task bar)
# uses chromedriver, not chrome

executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


# Navigate chromebrowser window to JPL images site
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)


# In[10]:


# Set a manual delay.
sleep(3) 


# In[11]:


# USE SPLINTER to navigate & store jpg url:

# Click on the FULL IMAGE link (in browser)
browser.links.find_by_partial_text("FULL IMAGE").click()


# In[12]:


# Set a manual delay.
sleep(3) 
# Click on the MORE INFO link (in browser)
browser.links.find_by_partial_text("more info").click()


# In[13]:


# Click on the JPEG image (in browser)
browser.links.find_by_partial_text(".jpg").click()


# In[14]:


# Save a variable of the URL of the JPEG image file 
featured_image_url = browser.url
featured_image_url


# In[15]:


# Close the chromebrowser window
browser.quit()


# In[16]:


##Mars Facts!

# use pandas to scrape Mars Data table (facts and structure)
# include 9 items: Equatorial Diameter, Polar diameter, mass,
# moons, orbit , orbit, surface temp, first record, recorded by


# In[17]:


# Define URL  (Mars Facts)
facts_url = "https://space-facts.com/mars/"

# Read in data table via Pandas. 
# >> Specify [0] position to get just Mars data 

facts_df = pd.read_html(facts_url)[0]


# In[18]:


# Create a polished dataframe with column headers and text clean-up
facts_df.columns = ["Metric", "Planet Mars"]

# Remove the colon character in DESCRIPTION column
facts_df["Metric"] = facts_df["Metric"].str.replace(":","") 

facts_df


# In[19]:


# Use Pandas to convert the data to a HTML table string
facts_df.set_index("Metric", inplace=True)

# print(facts_html)
facts_html = facts_df.to_html()


# In[20]:


## OVERVIEW: MARS HEMISPHERES
#  1. Visit USGS Astrogeology site & obstain hi res images for each of Mars' hemispheres
#  2. Click each link to open image url to full resolution
#  3. Save image url for full res image, and hemisphere tilte containing hemi. name. 
#   >> use a python dictionary to store the data using the keys "img_url" and "title"
#  4. Append the dictionary with the image url string and the hemisphere title to a list.
#     This list will contain one dictionary for each hemisphere


# In[36]:




# Open a new chrome browser window (and icon on task bar)
# uses chromedriver, not chrome
executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[37]:


# MARS HEMISPHERES, step-by-step
#  Visit USGS Astrogeology site & obstain hi res images for each of Mars' hemispheres
#def mars_hemisphere_function(browser):
    
# Navigate chromebrowser window to MARS HEMISPHERES website    
mars_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(mars_url)

# Set a manual delay.
sleep(3) 

# &run BeautifulSoup to parse the site's HTML
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[39]:


# Create dictionary for URLs & pics (empty); Create list for image URLs (empty); 
# Create list of hemisphere names (FILLED)
mars_dict = {}
mars_hemi_urls = []
mars_hemi = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]


# In[ ]:





# In[40]:


# Loop through hemispheres by name, populate dictionary with URL and pic
for hemi in mars_hemi:
    
    print(hemi)
    sleep(3)
    
    browser.links.find_by_partial_text(hemi).click()
    
    face_html = browser.html
    soup = BeautifulSoup(face_html, "html.parser")
    
    mars_dict["title"]= soup.find(
        "h2").get_text().replace("Enhanced","").strip()
    mars_dict["img_url"] = soup.find_all("div", class_="downloads")[0].find_all("a")[0]["href"]
    mars_hemi_urls.append(mars_dict)

# go back to main directory
    browser.back()

# view images URLs
#return mars_hemi_urls
# Close the chromebrowser window
#browser.quit()
                  


# In[41]:


print(mars_hemi_urls)


# In[ ]:


# STEP 2 ON TO MONGO DB & FLASK.....


# In[ ]:


# (convert Jupyter notebook to Python script with a function called "scrape"
# that will convert all of your scraping code from above and return one python dictionary 
# containing all of the scraped data
# >>The cleanest way is to just copy and paste code from jupyter notebook to a .py file <<
#
# NEXT in app.py file create a route called /scrape that will import scrape_mars.py script 
# and call your "scrape" function. Store your return value in Mongo as a Python dictionary.

# Create a root route / that will query your Mongo database and pass the mars data into 
# an HTML template to display the data.

# Create a template HTML file called "index.html" that will take the mars data dictionary
# and display all of the data in the appropriate HTML elements. Use the following as a guide
# for what the final product should look like, but feel free to create your own design. 
# >>As long as all the data is displayed, formatting and design are of secondary importance. <<
# Reminder that in order to interact correctly with flask, this HTML file must live in the
# templates folder that is located in the same folder as your app.py file. 
# Grab the latest headline

