from urllib.parse import urlparse
from url_normalize import url_normalize
from collections import defaultdict
from protego import Protego
from fetcher import Fetcher
from session import Session
import time
import random
import threading

class Frontier:
    def __init__(self):
        self.domain_last_access = {}
        self.session = Session()
        self.domain_delay = {}
        self.fetcher = Fetcher(self.session)
        self.frontier = defaultdict(list)
        self.lock = threading.Lock()
        self.visited = set()

    def add(self, url):
        domain = self.get_domain(url)
        if not self.can_crawl(url):
            return
        if url in self.visited:
            return
        
        self.frontier[domain].append(url)


    def can_crawl(self, url):
        rp = Protego.parse(url + "/robots.txt") 
        can_crawl = rp.can_fetch("*", url)

        if not can_crawl:
            return False

        return True

    def get_domain(self, url):
        normalized_url = url_normalize(url)
        domain = urlparse(normalized_url).netloc
        return domain

    def update(self, urls):
        with self.lock:
            for url in urls:
                self.add(url)

    def update_last_access(self, url, timestamp):
        domain = self.get_domain(url)

        with self.lock:
            if domain in self.domain_last_access:
                self.domain_last_access[domain] = max(self.domain_last_access.get(domain, 0), timestamp)

    def get_url(self):
        while True:
            now = time.time()

            with self.lock:
                domains = list(self.frontier.keys())
                random.shuffle(domains)
                for domain in domains:
                    if  not self.frontier[domain]:
                        del self.frontier[domain]
                        continue

                    last_access = self.domain_last_access.get(domain, 0)

                    if domain not in self.domain_delay:
                        self.domain_delay[domain] = self.fetcher.get_delay(domain)

                    delay = self.domain_delay.get(domain, 0.2)

                    if now - last_access >= delay:
                        idx = random.randrange(0, len(self.frontier[domain]))  
                        url = self.frontier[domain].pop(idx)

                        if not self.fetcher.can_crawl(url):
                            self.visited.add(url)
                            continue

                        if url  in self.visited:
                            continue

                        self.visited.add(url) 
                        return url, domain

            time.sleep(0.1)

    def fetch_error(self, url, timestamp):
        with self.lock:
            domain = self.get_domain(url)
            self.update_last_access(url, timestamp)
            self.visited.remove(url)
            self.frontier[domain].append(url)
