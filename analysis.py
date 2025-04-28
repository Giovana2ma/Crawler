from collections import defaultdict
from urllib.parse import urlparse

class Analysis:
    def __init__(self):
        self.domain_page_count = defaultdict(int)  # domain -> number of pages
        self.page_token_count = {}  # url -> number of tokens
        self.visited_urls = set()

    def add_page(self, url, text):
        if url in self.visited_urls:
            # Avoid double-counting
            return

        self.visited_urls.add(url)

        domain = self._extract_domain(url)
        token_count = self._count_tokens(text)

        self.domain_page_count[domain] += 1
        self.page_token_count[url] = token_count

    def _extract_domain(self, url):
        parsed = urlparse(url)
        return parsed.netloc

    def _count_tokens(self, text):
        return len(text.split())

    def report(self):
        report_data = {}

        report_data["total_unique_domains"] = len(self.domain_page_count)
        report_data["size_distribution_per_domain"] = dict(self.domain_page_count)
        report_data["size_distribution_per_page"] = dict(self.page_token_count)

        return report_data

    def print_report(self):
        data = self.report()
        print("\n=== Crawling Analysis Report ===")
        print(f"Total Unique Domains: {data['total_unique_domains']}")
        print("\nSize Distribution (pages per domain):")
        for domain, count in sorted(data['size_distribution_per_domain'].items(), key=lambda x: x[1], reverse=True):
            print(f" - {domain}: {count} page(s)")

        print("\nSize Distribution (tokens per page):")
        for url, tokens in sorted(data['size_distribution_per_page'].items(), key=lambda x: x[1], reverse=True):
            print(f" - {url}: {tokens} tokens")
        print("================================\n")
