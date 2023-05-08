# -*- coding:Utf8 -*-
#############################################
# Programme Python type
#############################################
from scrap import Scraper, URL
#############################################

if __name__ == '__main__':
    scraper = Scraper(URL)
    scraper.run_async()
