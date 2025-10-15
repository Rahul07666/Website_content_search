import requests
from bs4 import BeautifulSoup

def fetch_and_clean_html(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)

def search_chunks(chunks, query):
    results = []
    for chunk in chunks:
        if query.lower() in chunk.lower():
            results.append(chunk)
    return results[:10]

# Example
text = fetch_and_clean_html("https://example.com")
chunks = [text[i:i+500] for i in range(0, len(text), 500)]
matches = search_chunks(chunks, "sample")
print(matches)
