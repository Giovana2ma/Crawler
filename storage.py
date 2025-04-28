import os
import time
import logging
import threading
from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders
from io import BytesIO
from requests import Response

class Storage:
    NUM_RETRIES = 60

    def __init__(self, execution_id):
        self.lock = threading.RLock()
        self.output_dir = f"output/{execution_id}"
        self.count = 0
        
        os.makedirs(self.output_dir, exist_ok=True)

    def _build_http_response(self, response: Response) -> bytes:
        """Build a raw HTTP response (status line + headers + body)"""
        status_line = f"HTTP/1.1 {response.status_code} {response.reason}\r\n"
        headers = ''.join(f"{k}: {v}\r\n" for k, v in response.headers.items())
        full_response = (status_line + headers + "\r\n").encode('utf-8') + response.content
        return full_response

    def write(self, buffer):
        with self.lock:
            if len(buffer) == 0:
                return

            file_path = f"{self.output_dir}/output-{self.count}.warc.gz"

            with open(file_path, "wb") as stream:
                writer = WARCWriter(stream, gzip=True)
                for page in buffer:
                    http_response_bytes = self._build_http_response(page.content)

                    with BytesIO(http_response_bytes) as payload:
                        record = writer.create_warc_record(
                            page.url,
                            "response",
                            payload=payload
                        )
                        writer.write_record(record)

            self.count += 1
