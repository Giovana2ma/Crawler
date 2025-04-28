from url_normalize import url_normalize

def normalize_url(url):
    """
    Normalize a URL using url_normalize.
    Args:
        url (str): The URL to normalize.
    Returns:
        str: The normalized URL.
    """
    try:
        return url_normalize.url_normalize(url)
    except Exception as e:
        print(f"Error normalizing URL {url}: {e}")
        return url