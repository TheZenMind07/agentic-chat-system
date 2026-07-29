import { useState } from "react";

const API = "/api";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [uploading, setUploading] = useState(false);

  async function send(e) {
    e.preventDefault();
    const q = input.trim();
    if (!q || busy) return;
    setMessages((m) => [...m, { role: "user", text: q }]);
    setInput("");
    setBusy(true);
    try {
      const r = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      const data = await r.json();
      setMessages((m) => [...m, { role: "assistant", text: data.answer, sources: data.sources }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "assistant", text: `Error: ${err.message}` }]);
    } finally {
      setBusy(false);
    }
  }

  async function upload(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const r = await fetch(`${API}/ingest`, { method: "POST", body: fd });
      const data = await r.json();
      setMessages((m) => [...m, { role: "system", text: `Indexed ${data.filename}: ${data.chunks} chunks` }]);
    } catch (err) {
      setMessages((m) => [...m, { role: "system", text: `Upload failed: ${err.message}` }]);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Agentic Chat</h1>
        <label className="upload">
          {uploading ? "Uploading..." : "Upload doc"}
          <input type="file" accept=".pdf,.txt" hidden onChange={upload} />
        </label>
      </header>
      <main>
        {messages.length === 0 && (
          <div className="empty">Upload a document, then ask a question.</div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="bubble">{m.text}</div>
            {m.sources && m.sources.length > 0 && (
              <details className="sources">
                <summary>{m.sources.length} source(s)</summary>
                {m.sources.map((s, j) => (
                  <div key={j} className="source">
                    <strong>{s.source}</strong>
                    <p>{s.snippet}...</p>
                  </div>
                ))}
              </details>
            )}
          </div>
        ))}
      </main>
      <form onSubmit={send}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your docs..."
          disabled={busy}
        />
        <button disabled={busy || !input.trim()}>Send</button>
      </form>
    </div>
  );
}