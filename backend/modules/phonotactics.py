import re
import json
import os
from dataclasses import dataclass

@dataclass
class PhonError:
    word: str
    rule: str
    message: str

# Combinaisons INTERDITES en Malagasy
FORBIDDEN_PATTERNS = [
    (r'\bnb', "nb en début de mot interdit"),
    (r'\bmk', "mk en début de mot interdit"),
    (r'\bnk', "nk en début de mot interdit"),
    (r'dt', "combinaison 'dt' inexistante"),
    (r'bp', "combinaison 'bp' inexistante"),
    (r'sz', "combinaison 'sz' inexistante"),
    (r'mp$', "Un mot ne peut pas se terminer par 'mp'"), # Correction de la règle mp
]

class MalagasyPhonotactics:
    def __init__(self, dict_path="data/dataset.json"):
        # Calcul du chemin comme dans le spellchecker
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        absolute_path = os.path.join(base_dir, dict_path)
        
        try:
            with open(absolute_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # On stocke dans un set pour une recherche ultra-rapide O(1)
                # On gère le format liste simple ou liste d'objets
                if data and isinstance(data[0], dict):
                    self.dictionary = {item['mot'].lower() for item in data if 'mot' in item}
                else:
                    self.dictionary = {word.lower() for word in data}
        except Exception as e:
            print(f"Erreur chargement dictionnaire phonotactique: {e}")
            self.dictionary = set()

    def check_word(self, word: str) -> list[PhonError]:
        word_clean = word.lower().strip()
        
        # SI LE MOT EST DANS LE DICTIONNAIRE, ON NE CHERCHE PAS D'ERREUR
        # C'est une exception validée.
        if word_clean in self.dictionary:
            return []

        errors = []
        for pattern, message in FORBIDDEN_PATTERNS:
            if re.search(pattern, word_clean):
                errors.append(PhonError(word=word, rule=pattern, message=message))
        
        return errors

    def check_text(self, text: str) -> list[dict]:
        # Extraction des mots incluant les caractères spéciaux
        words = re.findall(r'\b[a-zA-ZàâéèêëîïôùûüÀÂÉÈÊËÎÏÔÙÛÜ’\']+\b', text)
        all_errors = []
        
        for word in words:
            errs = self.check_word(word)
            for e in errs:
                all_errors.append({
                    "word": e.word,
                    "rule": e.rule,
                    "message": e.message,
                    "type": "phonotactic"
                })
        return all_errors

# --- TEST ---
if __name__ == "__main__":
    # Supposons que 'dataset.json' contient "manasa"
    checker = MalagasyPhonotactics()
    
    # "nbaraka" n'est pas dans le dico et commence par nb -> Erreur
    # "manasa" est dans le dico -> Pas d'erreur même si on changeait les règles
    test_text = "nbaraka sy manasa"
    print(checker.check_text(test_text))