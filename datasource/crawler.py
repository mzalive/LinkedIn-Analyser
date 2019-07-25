from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv
import parameters
from time import sleep
import os
import random

# defining new variable passing two parameters
writer = csv.writer(open(parameters.file_name, 'wb'))
# writerow() method to the write to the file object
writer.writerow(['Name', 'Title', 'Location', 'Connection', 'Company', 'College', 'URL'])
# specifies the path to the chromedriver
print os.getcwd()
driver = webdriver.Chrome('../'+ parameters.driver_location)
# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/login')

# locate email form by_class_name
username = driver.find_element_by_id('username')
password = driver.find_element_by_id('password')
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

username.send_keys(parameters.linkedin_username)
password.send_keys(parameters.linkedin_password)

sleep(0.5)
sign_in_button.click()

# search on google
driver.get('https://www.google.com/')

# locate search form by_name
search_query = driver.find_element_by_name('q')
# send_keys() to simulate the search text key strokes
search_query.send_keys(parameters.search_query)
# send_keys() to simulate the return key
search_query.send_keys(Keys.RETURN)

# locate URL by_class_name
linkedin_urls = [url.text for url in driver.find_elements_by_class_name('iUh30')]

# clean extracted raw data
def clean_data(data, field=None):
    if data:
        data = data.strip()
        if field == 'connection':
            # only extract connection numbers
            data = data.split()[0]
    else:
        data = ''

    return data.encode('utf-8')

# For loop to iterate over each URL in the list
for linkedin_url in linkedin_urls:
    # get the profile URL
    driver.get(linkedin_url)
    # add a 5 second pause loading each URL
    sleep(round(random.uniform(0,5), 1))
    # assigning the source code for the webpage to variable sel
    source = Selector(text=driver.page_source)

    name         = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][1]/li[1]/text()').extract_first()
    title        = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][1]//following-sibling::h2/text()').extract_first()
    location     = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][2]/li[1]/text()').extract_first()
    connection   = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][2]/li[2]/span/text()').extract_first()
    company      = source.xpath('//*[contains(@class, "pv-top-card-v3--experience-list-item")][@data-control-name="position_see_more"]/span/text()').extract_first()
    college      = source.xpath('//*[contains(@class, "pv-top-card-v3--experience-list-item")][@data-control-name="education_see_more"]/span/text()').extract_first()

    # writing the corresponding values to the header
    writer.writerow([clean_data(name),
                     clean_data(title),
                     clean_data(location),
                     clean_data(connection, 'connection'),
                     clean_data(company),
                     clean_data(college),
                     clean_data(linkedin_url.encode('utf-8'))])