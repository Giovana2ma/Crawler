from crawler import Crawler
import time
from datetime import datetime

initial_urls = ["https://www.msn.com/pt-br/noticias",
"https://boaforma.abril.com.br/",
"https://www.tuasaude.com/"]

execution_id = datetime.now().strftime("%Y%m%d%H%M%S")
crawler = Crawler(initial_urls,execution_id,100000, max_workers=16)
crawler.crawl()

time.sleep(60)




crawler.stop()

# --- Run ---

