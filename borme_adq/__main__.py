import sys

from spider import run_spider
from scraper import run_scraper

if __name__ == "__main__":
    arguments = sys.argv
    try:
        if "SPIDER" in arguments:
            run_spider()
        elif "SCRAPER" in arguments:
            run_scraper()

    except Exception as e:
        print("Error: " + e)

  
  # python3 -m borme_adq SPIDER "YYYYMMDD"
  # python3 -m borme_adq SCRAPER params