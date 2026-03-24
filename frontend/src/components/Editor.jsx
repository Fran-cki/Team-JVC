import { useRef, useEffect } from "react";

export default function Editor({ text, onChange, predictions, onInsertPrediction, onPredict }) {
  const textareaRef = useRef(null);

  // Auto-resize du textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = ta.scrollHeight + "px";
    }
  }, [text]);

  const handleKeyUp = (e) => {
    // Déclenche la prédiction après un espace ou une ponctuation
    if (e.key === " " || e.key === "." || e.key === ",") {
      onPredict(text);
    }
  };

  return (
    <div className="editor-wrap">
      <div className="editor-inner">
        <div className="editor-header">
          <span className="editor-label">Document Malagasy</span>
          {/* <span className="editor-status">
            {text.split(/\s+/).filter(w => w.length > 0).length} mots
          </span> */}
        </div>

        <textarea
          ref={textareaRef}
          className="editor-textarea"
          value={text}
          onChange={(e) => onChange(e.target.value)}
          onKeyUp={handleKeyUp}
          placeholder="Soraty eto ny lahatsoratra..."
          spellCheck={false}
          autoComplete="off"
          id="textarea"
        />

        {/* Liste des suggestions style "Autocomplete" */}
        {predictions && predictions.length > 0 && (
          <div className="suggestion-bar">
            <div className="suggestion-content">
              {predictions.map((word, i) => (
                <button
                  key={i}
                  className="suggestion-item"
                  onClick={() => onInsertPrediction(document.getElementById("textarea").value+" "+word)}
                  title={`Insérer "${word}"`}
                >
                  <span className="suggestion-text">{word}</span>
                  {/* <kbd className="suggestion-key">{i}</kbd> */}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}