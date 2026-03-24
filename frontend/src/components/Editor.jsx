import { useRef, useEffect } from "react";

export default function Editor({ text, onChange, predictions, onInsertPrediction }) {
  const textareaRef = useRef(null);

  // Ajoutez 'predictions' dans le tableau de dépendances
  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto"; 
      // Le scrollHeight sera automatiquement contraint par le minHeight du CSS
      ta.style.height = ta.scrollHeight + "px";
    }
  }, [text, predictions]); // <--- On surveille aussi les suggestions ici

  // Fonction pour gérer l'insertion et le focus
  const handleSuggestionClick = (suggestion) => {
    // On construit la nouvelle valeur
    const newValue = text + " " + suggestion;
    
    // On appelle la fonction parente pour mettre à jour l'état
    onInsertPrediction(newValue);

    // ✅ FOCUS AUTOMATIQUE : On redonne le focus au textarea
    if (textareaRef.current) {
      textareaRef.current.focus();
      const length = textareaRef.current.value.length;
      textareaRef.current.setSelectionRange(length, length);
    }
  };

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
          style={{minHeight: (predictions.length > 0) ? "350px" : "420px"}}
        />

        {predictions.length > 0 && (
          <div className="predictions">
            <span className="predictions-label">Suggestions :</span>
            {predictions.map((w, i) => (
              <button
                key={i}
                type="button" // Important pour éviter les soumissions de formulaire accidentelles
                className="prediction-chip"
                onClick={() => handleSuggestionClick(w)}
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