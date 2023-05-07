# -*- coding:Utf8 -*-
#############################################
# Programme Python type
#############################################
from scrap.scraper import Scraper
from scrap.constantes import URL
#############################################

if __name__ == '__main__':
    scraper = Scraper(URL)
    scraper.run_async()
