from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from threading import Thread
import csv
import parameters
from time import sleep
import os
import random

class CrawlerStatus:
    IDLE = '0'
    RUNNING = '1'


class Crawler(Thread):
    def __init__(self):
        # add threading support
        Thread.__init__(self)
        # specifies the path to the chrome driver
        self.driver = None
        # current status
        self.current_status = CrawlerStatus.IDLE
        self.signal_continue = False

    # reset runtime flags
    def _pre_start_init(self):
        self.signal_continue = True
        # csv writer
        self.writer = self._init_output_file()
        # link of google search result next page
        self.google_next_page_link = None
        # number of profiles scraped
        self.count = 0

        # prepare driver
        if not self.driver:
            # headless chrome driver configure
            options = None
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=options, executable_path=parameters.driver_location)

    # sleep for a random waiting time, like a human
    def _pause_humanised(self):
        time = round(random.uniform(parameters.MIN_WAITING, parameters.MAX_WAITING), 1)
        sleep(time)


    # clean extracted raw data
    def _clean_data(self, data, field=None):
        if data:
            data = data.strip()
            if field == 'connection':
                # only extract connection numbers
                data = data.split()[0]
        else:
            data = ''

        return data.encode('utf-8')


    # prepare result file
    def _init_output_file(self):
        # test dir
        directory = os.path.dirname(parameters.path_to_results)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # init file
        writer = csv.writer(open(parameters.path_to_results, 'wb'))
        writer.writerow(['Name', 'Title', 'Location', 'Connection', 'Company', 'College', 'URL'])

        return writer

    # login linkedin
    def _linkedin_login(self):

        driver = self.driver

        driver.get('https://www.linkedin.com/login')

        # locate critical elements
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

        # fill in credentials
        username.send_keys(parameters.linkedin_username)
        password.send_keys(parameters.linkedin_password)

        # execute login
        self._pause_humanised()
        sign_in_button.click()

    # scrape linkedin profiles url on google
    def _scrape_profile_urls(self):

        driver = self.driver

        if not self.google_next_page_link:
            # first-time search
            driver.get('https://www.google.com/')

            # simulate search
            search_query = driver.find_element_by_name('q')
            search_query.send_keys(parameters.search_query)
            search_query.send_keys(Keys.RETURN)

        else:
            # continue for next page
            driver.get(self.google_next_page_link)

        # scrape urls
        linkedin_urls = [url.text for url in driver.find_elements_by_class_name('iUh30')]

        # save next page url
        self.google_next_page_link = driver.find_elements_by_id('pnnext')[0].get_attribute("href")

        return linkedin_urls



    def _crawl(self):

        self.current_status = CrawlerStatus.RUNNING

        driver = self.driver

        # login linkedin for the first time
        self._linkedin_login()

        # scrape url
        while self.count < parameters.CRAWL_LIMIT and self.signal_continue:

            # get a fresh list of profile urls
            linkedin_urls = self._scrape_profile_urls()

            # extract data of each profile
            for url in linkedin_urls:

                self.count += 1
                # pause before loading each URL
                self._pause_humanised()
                # open profile
                driver.get(url)
                source = Selector(text=driver.page_source)

                # parse desired elements
                name         = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][1]/li[1]/text()').extract_first()
                title        = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][1]//following-sibling::h2/text()').extract_first()
                location     = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][2]/li[1]/text()').extract_first()
                connection   = source.xpath('//*[contains(@class, "pv-top-card-v3--list")][2]/li[2]/span/text()').extract_first()
                company      = source.xpath('//*[contains(@class, "pv-top-card-v3--experience-list-item")][@data-control-name="position_see_more"]/span/text()').extract_first()
                college      = source.xpath('//*[contains(@class, "pv-top-card-v3--experience-list-item")][@data-control-name="education_see_more"]/span/text()').extract_first()

                # writing the corresponding values to the header
                self.writer.writerow([self._clean_data(name),
                                 self._clean_data(title),
                                 self._clean_data(location),
                                 self._clean_data(connection, 'connection'),
                                 self._clean_data(company),
                                 self._clean_data(college),
                                 self._clean_data(url.encode('utf-8'))])

                # print self._clean_data(name), self._clean_data(title), self._clean_data(location), self._clean_data(connection, 'connection'), self._clean_data(company), self._clean_data(college), self._clean_data(url.encode('utf-8'))

        # crawling finished or terminated
        self.driver.quit()
        self.current_status = CrawlerStatus.IDLE

    def run(self):
        # cold start
        if self.current_status == CrawlerStatus.IDLE:
            # init runtime parameters
            self._pre_start_init()
            # start crawling
            self._crawl()

    def stop(self):
        self.signal_continue = False

    # return status code & message to indicate running condition
    def status(self):
        if self.current_status == CrawlerStatus.RUNNING:
            return self.current_status, 'Running: {:d}'.format(self.count) if self.signal_continue else 'Terminating...'
        else:
            return self.current_status, 'Starting...' if self.signal_continue else 'Stopped.'



if __name__ == '__main__':
    crawler = Crawler()
    crawler.start()
    # print crawler.status()