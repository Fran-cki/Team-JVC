import { useRef, useEffect } from "react";

export default function Editor({ text, onChange, predictions, onInsertPrediction }) {
  const textareaRef = useRef(null);

  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = ta.scrollHeight + "px";
    }
  }, [text]);

  return (
    <div className="editor-wrap">
      <div className="editor-inner">
        <div className="editor-label">Document</div>
        <textarea
          ref={textareaRef}
          className="editor-textarea"
          value={text}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Écrire en malagasy ici…"
          spellCheck={false}
          autoComplete="off"
          id="textChamp"
        />

        {predictions.length > 0 && (
          <div className="predictions">
            <span className="predictions-label">Suggestions :</span>
            {predictions.map((w, i) => (
              <button
                key={i}
                className="prediction-chip"
                onClick={() => onInsertPrediction(document.getElementById("textChamp").value+" "+w)}
              >
                {w}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
