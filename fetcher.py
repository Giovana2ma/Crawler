from bs4 import BeautifulSoup
from url_normalize import url_normalize
import threading
from protego import Protego
import logging


class Fetcher():
    def __init__(self,session):
        self.session = session
        self.lock = threading.Lock()


    def fetch(self,url):
        """
        Fetches the page content using the Session instance.

        Returns:
            str or None: Raw HTML content if successful, else None.
        """
        try:
            response = self.session.get(url)

            if response is None:
                return None
            
            content_type = response.headers.get('Content-Type', '').lower()
            
            if 'text/html'  in content_type:
                return response
                
        except Exception as e:
            logging.error(f"Error fetching URL {url}: {e}")
            pass
        return None
        
    def get_content(self):
        title = self.soup.title.string if self.soup.title else ''
        content = self.soup.get_text()
        return title,content

    def get_links(self):
        links = []
        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('http'):
                try:
                    normalized_url = url_normalize(href)
                    links.append(normalized_url)
                except Exception as e:
                    logging.error(f"Error normalizing URL {href}: {e}")
                    pass
        return links

    def collect(self,url):
        with self.lock:
            response = self.fetch(url)

            if response is None:
                return None
            
            if response == -1:
                return -1
            
            page = response.text
            self.soup = BeautifulSoup(page,features="html.parser")
            title,content = self.get_content()
            links = self.get_links()

        return title,content,links,response
    
    
