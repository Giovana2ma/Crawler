import json
import time
import logging
import threading

class Debugger:
    def __init__(self, debug=False):
        self.debug = debug
        self.lock = threading.Lock()


        if self.debug:
            logging.info("[DEBUG] Debug mode is ON")

    def log(self, url, title, content):
        if not self.debug:
            return
        

        # Prepare the debug information
        debug_info = {
            "url": url,
            "title": title,
            "text": self.get_text(content),
            "timestamp": int(time.time())
        }

        logging.info(json.dumps(debug_info, ensure_ascii=False))

    def get_text(self, text):
        words = text.split()
        content = words[:20]
        return " ".join(content)
