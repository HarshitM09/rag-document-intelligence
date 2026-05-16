import React, { useState } from "react";
import { submitSearch, submitChat } from "./api";
import "./styles.css";

export default function App() {
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState("");
  const [results, setResults] = useState(null);

  const handleSearch = async () => {
    const response = await submitSearch(query);
    setResults(response);
  };

  const handleChat = async () => {
    const response = await submitChat(chat);
    setResults(response);
  };

  return (
    <div className="app-shell">
      <header>
        <h1>Enterprise RAG Document Intelligence</h1>
        <p>Semantic search, chat, and knowledge orchestration for enterprise documents.</p>
      </header>
      <section>
        <div className="card">
          <h2>Semantic Search</h2>
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search enterprise knowledge" />
          <button onClick={handleSearch}>Search</button>
        </div>
        <div className="card">
          <h2>Conversational AI</h2>
          <textarea value={chat} onChange={(e) => setChat(e.target.value)} placeholder="Ask the AI about indexed documents"></textarea>
          <button onClick={handleChat}>Ask</button>
        </div>
      </section>
      {results && (
        <section className="card output">
          <h3>Response</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </section>
      )}
    </div>
  );
}
