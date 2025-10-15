import { useState } from "react";
import "./App.css";

function App() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/search?url=${encodeURIComponent(url)}&query=${encodeURIComponent(query)}`
      );
      const data = await res.json();
      if (data.matches) {
        setResults(data.matches);
      } else {
        setResults([]);
      }
    } catch (err) {
      console.error(err);
      setResults([]);
    }
  };

  return (
    <div className="App">
      <h1>Website Content Search</h1>
      <p className="subtitle">Search through website content with precision</p>

      <div className="form">
        <input
          type="text"
          placeholder="Website URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <input
          type="text"
          placeholder="Search Query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {/* ---- Render results as cards here ---- */}
      <div className="results">
        {results.map((res, index) => (
          <div key={index} className="card">
            <p>{res.slice(0, 300)}{res.length > 300 ? "..." : ""}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

