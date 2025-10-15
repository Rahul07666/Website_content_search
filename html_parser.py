import requests
from bs4 import BeautifulSoup

def fetch_html(url: str) -> str:
    """Fetch HTML content from a given URL"""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; ContentFetcher/1.0)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Raise error if invalid URL or network issue
    return response.text

def clean_html(html_content: str) -> str:
    """Remove scripts, styles, and extract clean text"""
    soup = BeautifulSoup(html_content, "lxml")

    # Remove unnecessary tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Get visible text
    text = soup.get_text(separator="\n", strip=True)

    # Clean multiple newlines/spaces
    clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
    return clean_text

if __name__ == "__main__":
    # Test example
    test_url = "https://example.com"
    html_data = fetch_html(test_url)
    clean_text = clean_html(html_data)
    print(clean_text[:1000])  # print first 1000 chars
