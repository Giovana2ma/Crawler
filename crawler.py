import threading
from frontier import Frontier
from fetcher import Fetcher
from session import Session
from storage import Writer
import time

class Crawler:
    def __init__(self, seeds, execution_id, limit, max_workers=5):
        self._finished_event = threading.Event()
        self.limit = limit
        self.execution_id = execution_id
        self.frontier = Frontier()
        self.session = Session()
        self.writer = Writer(execution_id, limit, self._finished_event)
        self.domain_fetchers = {}
        self.max_workers = max_workers
        self.threads = []
        self.seeds = seeds
        self.lock = threading.Lock()
        self.count = 0

    def get_fetcher(self, domain):
        with self.lock:
            if domain not in self.domain_fetchers:
                self.domain_fetchers[domain] = Fetcher(self.session)
            return self.domain_fetchers[domain]

    def _crawl(self):

        while not self._finished_event.is_set():
            url,domain = self.frontier.get_url()

            if url is None:
                time.sleep(0.1)
                continue

            fetcher = self.get_fetcher(domain) 
            result = fetcher.collect(url)

            if result is None:
                continue


            title, content, links,response = result
            print(f"[{threading.current_thread().name}] Fetched: {url} (Title: {title})")
    
            # Update frontier with newly discovered links
            timestamp = time.time()
            self.frontier.update_last_access(url, timestamp)
            self.frontier.update(links)
            self.writer.write(url, response)
        

        return
        


    def crawl(self):
        self.frontier.update(self.seeds)

        threads = []
            
        for i in range(self.max_workers):
            thread = threading.Thread(target=self._crawl, name=f"Worker-{i}")
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
            

    def stop(self):
        self.running = False
        for t in self.threads:
            t.join()
