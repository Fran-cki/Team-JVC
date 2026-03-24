const PANELS = [
  { id: "spell", label: "Orthographe", icon: "✦" },
  { id: "lemma", label: "Lemmes", icon: "◈" },
];

export default function Sidebar({ activePanel, onPanelChange, spellErrors, lemmaResults, loading }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-tabs">
        {PANELS.map((p) => (
          <button
            key={p.id}
            className={`sidebar-tab ${activePanel === p.id ? "active" : ""}`}
            onClick={() => onPanelChange(p.id)}
          >
            <span className="tab-icon">{p.icon}</span>
            {p.label}
          </button>
        ))}
      </div>

      <div className="sidebar-content">
        {activePanel === "spell" && (
          <SpellPanel errors={spellErrors} loading={loading.spell} />
        )}
        {activePanel === "lemma" && (
          <LemmaPanel results={lemmaResults} loading={loading.lemma} />
        )}
      </div>
    </aside>
  );
}

function SpellPanel({ errors, loading }) {
  if (loading) return <div className="panel-loading"><span className="spinner large" /></div>;
  if (!errors.length)
    return (
      <div className="panel-empty">
        <div className="empty-icon">✓</div>
        <p>Aucune erreur détectée</p>
        <span>Cliquez sur «&nbsp;Orthographe&nbsp;» pour vérifier</span>
      </div>
    );
  return (
    <div className="panel-list">
      <div className="panel-count">{errors.length} erreur{errors.length > 1 ? "s" : ""}</div>
      {errors.map((err, i) => (
        <div key={i} className="error-card">
          <div className="error-word">{err.word ?? err}</div>
          {err.suggestions && (
            <div className="error-suggestions">
              {err.suggestions.map((s, j) => (
                <span key={j} className="sug-chip">{s}</span>
              ))}
            </div>
          )}
          {err.message && <div className="error-msg">{err.message}</div>}
        </div>
      ))}
    </div>
  );
}

function LemmaPanel({ results, loading }) {
  if (loading) return <div className="panel-loading"><span className="spinner large" /></div>;
  if (!results.length)
    return (
      <div className="panel-empty">
        <div className="empty-icon">◈</div>
        <p>Aucun résultat</p>
        <span>Cliquez sur «&nbsp;Lemmatiser&nbsp;» pour analyser</span>
      </div>
    );
  return (
    <div className="panel-list">
      <div className="panel-count">{results.length} mot{results.length > 1 ? "s" : ""} analysé{results.length > 1 ? "s" : ""}</div>
      {results.map((r, i) => (
        <div key={i} className="lemma-card">
          <div className="lemma-word">{r.word ?? Object.values(r)[0]}</div>
          <div className="lemma-meta">
            {r.lemma && <span className="lemma-tag lemma">{r.lemma}</span>}
            {r.pos && <span className="lemma-tag pos">{r.pos}</span>}
            {r.root && <span className="lemma-tag root">{r.root}</span>}
          </div>
        </div>
      ))}
    </div>
  );
}
