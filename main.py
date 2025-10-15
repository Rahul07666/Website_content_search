from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---- CORS setup ----
origins = [
    "http://localhost:3000",  # React dev server
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Function to fetch and clean HTML ----
def fetch_and_clean_html(url: str) -> str:
    """Fetch website HTML and clean text content"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts, styles, and other non-content tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "svg", "img"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())  # clean extra spaces
    print("Fetched text preview:", text[:300])
    return text


# ---- Function to split text into readable chunks ----
def chunk_text(text: str, chunk_size: int = 600):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks


# ---- Function to search for query ----
def search_chunks(chunks, query):
    query_lower = query.lower()
    results = [chunk for chunk in chunks if query_lower in chunk.lower()]
    return results[:10]


# ---- Main API Endpoint ----
@app.get("/search")
def search(url: str = Query(...), query: str = Query(None)):
    """
    1. If only URL is given: return 10 random or first chunks from the site.
    2. If query is given: return top 10 chunks that contain the query.
    """
    try:
        # Step 1: Fetch website text
        text = fetch_and_clean_html(url)
        chunks = chunk_text(text, chunk_size=600)

        # Step 2: Handle both cases
        if query and query.strip():
            results = search_chunks(chunks, query)
            message = f"Top 10 matches for '{query}' on {url}"
        else:
            # return top 10 chunks from the site
            results = chunks[:10]
            message = f"Top 10 content chunks from {url}"

        if not results:
            return {"matches": ["No results found."], "message": message}

        return {"matches": results, "message": message}

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}
