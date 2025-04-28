from urllib.parse import urlparse
from url_normalize import url_normalize
from collections import defaultdict
from protego import Protego
import time
import random
import threading

class Frontier:
    def __init__(self):
        self.domain_last_access = {}
        self.domain_in_use = {}
        self.domain_delay = {}

        self.domain_errorr = {}
        self.baned_domains = set()

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

    def error(self, domain):
        with self.lock:
            if domain in self.domain_errorr:
                self.domain_errorr[domain] += 1
            else:
                self.domain_errorr[domain] = 1

            if self.domain_errorr[domain] >= 5:
                self.baned_domains.add(domain)
                self.domain_errorr.pop(domain, None)
                self.frontier.pop(domain, None)
                self.domain_last_access.pop(domain, None)
                self.domain_delay.pop(domain, None)
                self.domain_in_use.pop(domain, None)


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

    def update_urls(self, urls):
        with self.lock:
            for url in urls:
                self.add(url)

    def update_last_access(self, url, timestamp):
        domain = self.get_domain(url)

        with self.lock:
            if domain in self.domain_last_access:
                self.domain_last_access[domain] = max(self.domain_last_access.get(domain, 0), timestamp)
    
    def get_delay(self, domain):
        rp = Protego.parse(domain + "/robots.txt") 
        delay = rp.crawl_delay("*")

        if delay is None:
            return  0.2
        else:
            return delay

    def can_crawl(self, url):
        rp = Protego.parse(url + "/robots.txt") 
        can_crawl = rp.can_fetch("*", url)

        if not can_crawl:
            return False

        return True
    
    def update_use(self,domain):
        with self.lock:
            self.domain_in_use[domain] = False

    def get_url(self):
        while True:
            now = time.time()

            with self.lock:
                domains = list(self.frontier.keys())
                random.shuffle(domains)
                for domain in domains:
                    if domain not in self.domain_in_use:
                        self.domain_in_use[domain] = False

                    if self.domain_in_use[domain]:
                        continue

                    if  not self.frontier[domain]:
                        del self.frontier[domain]
                        continue

                    last_access = self.domain_last_access.get(domain, 0)

                    if domain not in self.domain_delay:
                        self.domain_delay[domain] = self.get_delay(domain)

                    delay = self.domain_delay.get(domain, 0.2)

                    if now - last_access >= delay:
                        idx = random.randrange(0, len(self.frontier[domain]))  
                        url = self.frontier[domain].pop(idx)

                        if not self.can_crawl(url):
                            self.visited.add(url)
                            continue

                        if url  in self.visited:
                            continue

                        self.visited.add(url) 
                        self.domain_in_use[domain] = True
                        return url, domain

