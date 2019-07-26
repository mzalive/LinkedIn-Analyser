# LinkedIn Analyser
## Overview
- Crawling Linkedin Profiles without official API.
- Simple Cluster Analysis on scraped data.
- Flask RESTFul API.
- Simple frontend for data visualisation & crawler management.


## Demo
Live demo at: `https://mzalive.org/linkedin-analyser/`

Note:
1. `Demo` dataset is pre crawled using the same module in the system, consists 100 linkedin profiles.
2. You can start / stop the crawler via the front-end panel, crawled data stored as the `crawled` dataset, each time the crawler starts, the crawler's data is erased.

## Run locally
### Back-end
Requirement: Python 2.7

1. Fill-in your linkedin credentials in `server/datasource/parameters.py `, this is required for linkedin crawler to work decently.
You may want to use a one-time account to do this as there is risks of getting banned.
2. The crawler use `Selenium` and `Chromedriver` to simulate human browsing. Therefore Chrome browser is necessary.
3. `Chromedriver` (http://chromedriver.chromium.org/), placed at `/service/static` is os-dependent, if you find it unable to start, try replace it.
4. Run `$ pip install -r requirements.txt` to install dependencies.
5. Run `$ pyhton app.py` to start back-end service on your local machine.

### Front-end

1. After you start the back-end service, open `web/js/main.js`, you'll find the api root url at the top. 
Replace the `api_base_url` filed to reflect the local back-end server you just started.
2. Copy the `web` directory to a working directory of any http server and serve.

## Credits
- Crawler: [David Craven](https://github.com/dcraven02): [Use Selenium & Python to scrape LinkedIn profiles](https://medium.com/@dcraven02/how-easy-it-is-to-scrape-linkedin-profiles-lets-find-out-ce82685d0a91)