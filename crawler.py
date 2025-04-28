import threading
from frontier import Frontier
from fetcher import Fetcher
from session import Session
from storage import Storage
from debugger import Debugger
from analysis import Analysis

import time

class Page:
    def __init__(self, url, content):
        self.url = url
        self.content = content

class Crawler:
    def __init__(self, seeds,max_workers,execution_id,debugger_mode,limit=100000):
        self.seeds = seeds
        self.count = 0
        self.fetchers = {}  
        self.buffer = []

        self.max_workers = max_workers
        self.execution_id = execution_id
        self.limit = limit

        self.running = True
        self.domain_locks = {}
        self.threads = []
        self.lock = threading.Lock()

        self.frontier = Frontier()
        self.session = Session()
        self.storage = Storage(execution_id)
        self.analysis = Analysis()
        self.debugger = Debugger(debugger_mode)

    def get_lock(self, domain):
        if domain not in self.domain_locks:
            self.domain_locks[domain] = threading.Lock()
        return self.domain_locks[domain]

    def _crawl(self):

        thread_id = threading.get_ident()
        fetcher = Fetcher(self.session)  # Each thread creates its own Fetcher
        self.fetchers[thread_id] = fetcher

        while self.running:
            url, domain = self.frontier.get_url()

            domain_lock = self.get_lock(domain) 
            with domain_lock:
                result = fetcher.collect(url)
                self.frontier.update_use(domain)

            if result is None:
                self.frontier.error(domain)
                continue


            title, content, links, response = result
            self.analysis.add_page(url, content)
            self.debugger.log(url, title, content)
    
            timestamp = time.time()
            self.frontier.update_last_access(url, timestamp)
            self.frontier.update_urls(links)

            if self.running:
                page = Page(url, response)
                self.store_content(page)
        
        return

    def store_content(self, content):
        with self.lock:
            if self.count % 10 == 0:
                self.storage.write(self.buffer)
                self.buffer = []

            if self.count >= self.limit:
                self.running = False
                return
            
            self.buffer.append(content)
            self.count += 1

    def crawl(self):
        self.frontier.update_urls(self.seeds)

        for i in range(self.max_workers):
            thread = threading.Thread(target=self._crawl, name=f"Worker-{i}")
            self.threads.append(thread)
            thread.start()
        
        for thread in self.threads:
            thread.join()
        
        # self.analysis.print_report()

