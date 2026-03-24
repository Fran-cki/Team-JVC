import { useState, useRef, useCallback, useEffect } from "react";
import Editor from "./components/Editor";
import Sidebar from "./components/Sidebar";
import StatusBar from "./components/StatusBar";
import "./App.css";

const API_BASE = "http://localhost:8080";

export default function App() {
  const [text, setText] = useState("");
  const [spellErrors, setSpellErrors] = useState([]);
  const [lemmaResults, setLemmaResults] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [activePanel, setActivePanel] = useState("spell");
  const [loading, setLoading] = useState({ spell: false, lemma: false, predict: false });
  const [wordCount, setWordCount] = useState(0);
  const debounceRef = useRef(null);

  useEffect(() => {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    setWordCount(words);
  }, [text]);

  const fetchPredictions = useCallback(async (val) => {
    if (!val.trim()) { setPredictions([]); return; }
    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: val }),
      });
      const data = await res.json();
      setPredictions(data.suggestions || []);
    } catch { setPredictions([]); }
  }, []);

  const handleTextChange = useCallback((val) => {
    setText(val);
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => fetchPredictions(val), 100);
  }, [fetchPredictions]);

  const runSpellCheck = async () => {
    if (!text.trim()) return;
    setLoading(l => ({ ...l, spell: true }));
    setActivePanel("spell");
    try {
      const res = await fetch(`${API_BASE}/spell-check`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setSpellErrors(data.errors || []);
    } catch { setSpellErrors([]); }
    setLoading(l => ({ ...l, spell: false }));
  };

  const runLemmatize = async () => {
    if (!text.trim()) return;
    setLoading(l => ({ ...l, lemma: true }));
    setActivePanel("lemma");
    try {
      const res = await fetch(`${API_BASE}/lemmatize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setLemmaResults(data.results || []);
    } catch { setLemmaResults([]); }
    setLoading(l => ({ ...l, lemma: false }));
  };

  const insertPrediction = (word) => {
    const trimmed = text.trimEnd();
    const lastSpace = trimmed.lastIndexOf(" ");
    const base = lastSpace >= 0 ? trimmed.slice(0, lastSpace + 1) : "";
    setText(word + " ");
    setPredictions([]);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="logo">
          <span className="logo-mg">MG</span>
          <span className="logo-text">Éditeur Malagasy</span>
        </div>
        <nav className="toolbar">
          <button
            className={`toolbar-btn ${loading.spell ? "loading" : ""}`}
            onClick={runSpellCheck}
            title="Vérification orthographique"
          >
            {loading.spell ? <span className="spinner" /> : "✦"}
            <span>Orthographe</span>
          </button>
          <button
            className={`toolbar-btn ${loading.lemma ? "loading" : ""}`}
            onClick={runLemmatize}
            title="Lemmatisation"
          >
            {loading.lemma ? <span className="spinner" /> : "◈"}
            <span>Lemmatiser</span>
          </button>
        </nav>
      </header>

      <main className="app-body">
        <Editor
          text={text}
          onChange={handleTextChange}
          predictions={predictions}
          onInsertPrediction={insertPrediction}
        />
        <Sidebar
          activePanel={activePanel}
          onPanelChange={setActivePanel}
          spellErrors={spellErrors}
          lemmaResults={lemmaResults}
          loading={loading}
        />
      </main>

      <StatusBar wordCount={wordCount} charCount={text.length} />
    </div>
  );
}
