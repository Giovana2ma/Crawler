import requests

class Session:
    def __init__(self, request_limit=500):
        """
        Initializes a new session.

        Args:
            request_limit (int): Maximum number of requests before resetting the session.
        """
        self.request_limit = request_limit
        self.request_count = 0
        self.session = requests.Session()

    def _reset_session(self):
        """
        Closes the current session and starts a new one.
        """
        self.session.close()
        self.session = requests.Session()
        self.request_count = 0

    def get(self, url):
        """
        Sends a GET request, managing session reset when needed.

        Args:
            url (str): The URL to fetch.

        Returns:
            requests.Response: The response object.
        """
        if self.request_count >= self.request_limit:
            self._reset_session()

        response = self.session.get(url, timeout= 0.5)
        self.request_count += 1
        return response
        