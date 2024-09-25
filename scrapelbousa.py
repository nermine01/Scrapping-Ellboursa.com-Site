#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pandas as pd

import time

start_time = time.time()


def scrape_ilboursa(start_date, days_to_scrape):
    base_url = "https://www.ilboursa.com/marches/actualites_bourse_tunis"

    # Set up the Selenium WebDriver (you need to have ChromeDriver installed)
    driver = webdriver.Chrome()

    data = {'date': [], 'article': []}

    try:
        for _ in range(days_to_scrape):
            formatted_date = start_date.strftime("%m/%d/%Y")

            # Navigate to the URL
            driver.get(base_url)

            # Wait for the date field to be present
            date_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "dateActu"))
            )

            # Set the date in the date field (respecting the French format)
            date_field.clear()
            date_field.send_keys(formatted_date)

            # Click the "Afficher" button
            afficher_button = driver.find_element(By.ID, "btn")
            afficher_button.click()

            # Allow some time for the page to load (adjust this if needed)
            time.sleep(4)

            # Get the page source after dynamic content has loaded
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract relevant information here based on the HTML structure of the page
            articles = soup.select('#tabQuotes tbody tr')  # Selecting all rows inside the table

            for article in articles:
                date_element = article.select_one('td span.sp1')
                if date_element:
                    date = date_element.text.strip()
                else:
                    date = "Unknown"

                article_link_element = article.select_one('td a[href^="/marches/"]')
                if article_link_element:
                    article_link = "https://www.ilboursa.com" + article_link_element['href']
                    article_name = article_link_element.text.strip()
                else:
                    article_link = "Unknown"
                    article_name = "Unknown"

                data['date'].append(date)
                data['article'].append({'name': article_name, 'link': article_link})

            # Move to the previous day
            start_date -= timedelta(days=1)

    finally:
        # Close the WebDriver
        driver.quit()

    return pd.DataFrame(data)

# Set the start date to today and specify the number of days to scrape (10 in this case)
start_date = datetime.now()
days_to_scrape = 3000

# Scrape the data and create a DataFrame
df = scrape_ilboursa(start_date, days_to_scrape)
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
# Print the DataFrame
df.head(20)


# In[5]:


df.to_csv('df.csv', index=False)
from IPython.display import FileLink

# Create a link to download the file
FileLink(r'df.csv')  


# In[7]:


df.to_xls('df.xls', index=False)
from IPython.display import FileLink

# Create a link to download the file
FileLink(r'df.xls') 


# In[ ]:




