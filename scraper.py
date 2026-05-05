import httpx
from bs4 import BeautifulSoup
import feedparser
import time
import random
import logging
from typing import List, Dict, Optional
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

class OpportunityScraper:
    def __init__(self):
        self.client = httpx.Client(timeout=30.0, follow_redirects=True)
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }

    def _get_headers(self):
        headers = self.headers.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        return headers

    def _delay(self):
        time.sleep(random.uniform(1, 3))

    def scrape_f6s(self, keyword: str, region: Optional[str] = None) -> List[Dict]:
        results = []
        try:
            for page in range(1, 4):
                url = f"https://www.f6s.com/programs?page={page}"
                if keyword:
                    url += f"&query={keyword}"
                
                logger.info(f"Scraping F6S: {url}")
                response = self.client.get(url, headers=self._get_headers())
                if response.status_code != 200:
                    logger.warning(f"F6S returned status {response.status_code}")
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                # F6S structure analysis (simulated based on typical structure)
                programs = soup.select('.program-item, .item-list-row')
                if not programs:
                    logger.warning(f"No programs found on F6S page {page}")
                    break

                for prog in programs:
                    title_elem = prog.select_one('.title a, .name a')
                    if not title_elem: continue
                    
                    title = title_elem.get_text(strip=True)
                    link = "https://www.f6s.com" + title_elem['href'] if title_elem['href'].startswith('/') else title_elem['href']
                    
                    organizer = prog.select_one('.organizer, .company-name').get_text(strip=True) if prog.select_one('.organizer, .company-name') else "Unknown"
                    location = prog.select_one('.location').get_text(strip=True) if prog.select_one('.location') else "Remote/Global"
                    deadline = prog.select_one('.deadline, .date').get_text(strip=True) if prog.select_one('.deadline, .date') else "Rolling"
                    desc = prog.select_one('.description, .summary').get_text(strip=True) if prog.select_one('.description, .summary') else ""

                    if region and region.lower() not in location.lower():
                        continue

                    results.append({
                        "title": title,
                        "type": "Accelerator", # F6S is primarily accelerators
                        "organizer": organizer,
                        "location": location,
                        "deadline": deadline,
                        "source_link": link,
                        "source_name": "F6S",
                        "description": desc,
                        "keyword_matched": keyword
                    })
                self._delay()
        except Exception as e:
            logger.error(f"Error scraping F6S: {e}")
        return results

    def scrape_devpost(self, keyword: str) -> List[Dict]:
        results = []
        try:
            for page in range(1, 4):
                url = f"https://devpost.com/hackathons?page={page}"
                if keyword:
                    url += f"&search={keyword}"
                
                logger.info(f"Scraping Devpost: {url}")
                response = self.client.get(url, headers=self._get_headers())
                if response.status_code != 200:
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                hackathons = soup.select('.hackathon-tile')
                if not hackathons:
                    break

                for hack in hackathons:
                    title_elem = hack.select_one('.title')
                    if not title_elem: continue
                    
                    title = title_elem.get_text(strip=True)
                    link = hack.select_one('a')['href']
                    organizer = hack.select_one('.organizer').get_text(strip=True) if hack.select_one('.organizer') else "Devpost Host"
                    location = hack.select_one('.location').get_text(strip=True) if hack.select_one('.location') else "Online"
                    deadline = hack.select_one('.submission-period').get_text(strip=True) if hack.select_one('.submission-period') else "TBA"
                    prizes = hack.select_one('.prizes').get_text(strip=True) if hack.select_one('.prizes') else ""

                    results.append({
                        "title": title,
                        "type": "Competition",
                        "organizer": organizer,
                        "location": location,
                        "deadline": deadline,
                        "source_link": link,
                        "source_name": "Devpost",
                        "description": f"Hackathon on Devpost. Prizes: {prizes}",
                        "keyword_matched": keyword
                    })
                self._delay()
        except Exception as e:
            logger.error(f"Error scraping Devpost: {e}")
        return results

    def scrape_grants_gov(self) -> List[Dict]:
        results = []
        try:
            url = "https://www.grants.gov/rss/GG_NewOpp.xml"
            logger.info(f"Parsing Grants.gov RSS: {url}")
            feed = feedparser.parse(url)
            
            for entry in feed.entries:
                results.append({
                    "title": entry.title,
                    "type": "Grant",
                    "organizer": "US Federal Government",
                    "location": "USA",
                    "deadline": entry.get('published', 'See link'),
                    "source_link": entry.link,
                    "source_name": "Grants.gov",
                    "description": entry.summary if 'summary' in entry else entry.title,
                    "keyword_matched": "US Government Grant"
                })
        except Exception as e:
            logger.error(f"Error parsing Grants.gov: {e}")
        return results

    def scrape_ycombinator(self) -> List[Dict]:
        # Using YC's public "Work at a Startup" or just general YC news as a placeholder for "Startup Source"
        # Let's use AlphaGamma as requested in my thought process or similar
        results = []
        try:
            # Example: AlphaGamma Opportunities
            url = "https://www.alphagamma.eu/category/opportunities/feed/"
            logger.info(f"Parsing AlphaGamma RSS: {url}")
            feed = feedparser.parse(url)
            
            for entry in feed.entries:
                results.append({
                    "title": entry.title,
                    "type": "Other",
                    "organizer": "AlphaGamma",
                    "location": "Global",
                    "deadline": "See link",
                    "source_link": entry.link,
                    "source_name": "AlphaGamma",
                    "description": entry.summary if 'summary' in entry else entry.title,
                    "keyword_matched": "Startup Opportunity"
                })
        except Exception as e:
            logger.error(f"Error parsing AlphaGamma: {e}")
        return results

    def scrape_all(self, keyword: str = "AI startup", region: Optional[str] = None) -> List[Dict]:
        all_results = []
        
        # Source 1: F6S
        all_results.extend(self.scrape_f6s(keyword, region))
        
        # Source 2: Devpost
        all_results.extend(self.scrape_devpost(keyword))
        
        # Source 3: AlphaGamma (RSS)
        all_results.extend(self.scrape_ycombinator())
        
        # Source 4: Grants.gov (RSS)
        all_results.extend(self.scrape_grants_gov())
        
        # Deduplication and filtering
        unique_results = {}
        for res in all_results:
            # Simple keyword filter if not already handled by source
            if keyword.lower() not in res['title'].lower() and keyword.lower() not in res['description'].lower():
                # For RSS feeds, we might need to filter manually
                if res['source_name'] in ["Grants.gov", "AlphaGamma"]:
                    continue
            
            if res['source_link'] not in unique_results:
                unique_results[res['source_link']] = res
        
        return list(unique_results.values())
