export default function StatusBar({ wordCount, charCount }) {
  return (
    <footer className="status-bar">
      <span className="status-item">
        <span className="status-val">{wordCount}</span> mot{wordCount !== 1 ? "s" : ""}
      </span>
      <span className="status-sep">·</span>
      <span className="status-item">
        <span className="status-val">{charCount}</span> caractère{charCount !== 1 ? "s" : ""}
      </span>
      <span className="status-sep">·</span>
      <span className="status-item api">API <span className="api-dot" /> localhost:8000</span>
    </footer>
  );
}
