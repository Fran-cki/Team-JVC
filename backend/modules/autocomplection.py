import json
import os

class MalagasyInferenceEngine:
    def __init__(self, model_path="data/model_ngram.json"):
        self.model = {}
        self.load_model(model_path)

    def load_model(self, path):
        """Charge les probabilités depuis le fichier JSON."""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.model = json.load(f)
            print("🚀 Moteur de prédiction chargé et prêt.")
        else:
            print("⚠️ Erreur : Fichier modèle introuvable.")

    def predict(self, text: str, limit=5):
        """
        Prend un texte en entrée, extrait le dernier mot 
        et suggère les mots suivants.
        """
        if not text:
            return []

        # Extraire le dernier mot (nettoyage rapide)
        words = text.lower().strip().split()
        if not words:
            return []
            
        last_word = words[-1]

        # Recherche dans le modèle
        if last_word in self.model:
            # Récupérer les mots et les trier par fréquence
            next_words = self.model[last_word]
            # Trier par valeur (fréquence) décroissante
            sorted_suggestions = sorted(next_words.items(), key=lambda item: item[1], reverse=True)
            return [word for word, count in sorted_suggestions[:limit]]
        
        return []

# --- EXEMPLE D'UTILISATION (TEST) ---
# moteur = MalagasyInferenceEngine("model_ngram.json")
# print(moteur.predict("isika dia")) 
# Sortie attendue : ['mandeha', 'faly', 'tia', ...]