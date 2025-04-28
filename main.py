from crawler import Crawler
from debugger import Debugger
import time
from utils import *
from datetime import datetime
import logging

args = parse_arguments()

seeds = load_seeds(args.seeds)
limit = args.limit
debug_mode = args.debug

log_level = logging.CRITICAL

if debug_mode:  
    log_level = logging.INFO
logging.basicConfig(level=log_level)

execution_id = datetime.now().strftime("%Y%m%d%H%M%S")
crawler = Crawler(seeds,16,execution_id,debug_mode,limit)
crawler.crawl()

# --- Run ---

