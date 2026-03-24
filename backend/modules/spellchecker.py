from rapidfuzz.distance import Levenshtein
import json, re, os

class MalagasySpellChecker:
    def __init__(self, dict_path="data/dictionary.json"):
        # Utilisation d'un chemin absolu pour éviter le FileNotFoundError
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = os.path.join(base_dir, dict_path)
        
        if not os.path.exists(absolute_path):
            # Fallback si le dossier data est au même niveau
            absolute_path = os.path.join(os.getcwd(), dict_path)

        with open(absolute_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Correction CRITIQUE : Extraire la valeur 'mot' car 'item' est un dict
            # Un set ne peut pas contenir de dict (unhashable)
            self.dictionary = {item['mot'].lower() for item in data}

    def is_valid(self, word: str) -> bool:
        """Vérifie si un mot existe dans le dictionnaire (Table de hachage)."""
        return word.lower() in self.dictionary

    def suggest(self, word: str, max_suggestions=5) -> list[str]:
        """
        Propose des corrections basées sur la distance de Levenshtein.
        """
        word = word.lower()
        if self.is_valid(word) or not self.dictionary:
            return []

        # 1. Filtrage par longueur (optimisation)
        # On ne compare que les mots ayant une longueur proche (+/- 2 caractères)
        candidates = [
            w for w in self.dictionary 
            if abs(len(w) - len(word)) <= 2
        ]

        # 2. Calcul des distances
        scored = [
            (w, Levenshtein.distance(word, w))
            for w in candidates
        ]

        # 3. Tri par score (le plus proche en premier)
        scored.sort(key=lambda x: x[1])

        # 4. Retourne les suggestions les plus pertinentes (distance max de 3)
        return [w for w, d in scored[:max_suggestions] if d <= 3]

    def check_text(self, text: str) -> list[dict]:
        """
        Analyse un texte complet et retourne les erreurs détectées.
        """
        # Regex pour extraire les mots (incluant les caractères accentués malgaches)
        words = re.findall(r'\b[a-zA-ZàâéèêëîïôùûüÀÂÉÈÊËÎÏÔÙÛÜ’\']+\b', text)
        errors = []
        seen_in_text = {} # Cache local pour ne pas recalculer le même mot deux fois

        for word in words:
            word_lower = word.lower()
            if not self.is_valid(word_lower):
                if word_lower not in seen_in_text:
                    seen_in_text[word_lower] = self.suggest(word_lower)
                
                errors.append({
                    "word": word,
                    "suggestions": seen_in_text[word_lower],
                    "index": text.find(word) # Optionnel : pour le soulignement dans l'UI
                })
        
        return errors

# --- Exemple d'utilisation ---
if __name__ == "__main__":
    # Assure-toi que le chemin vers ton dataset.json est correct
    checker = MalagasySpellChecker(dict_path="data/dataset.json")
    
    test_phrase = "Aho ianao sy izy ireo ety" # 'ety' au lieu de 'ery' ou 'eto'
    results = checker.check_text(test_phrase)
    
    for err in results:
        print(f"Erreur détectée : '{err['word']}'")
        print(f"Suggestions : {', '.join(err['suggestions'])}")