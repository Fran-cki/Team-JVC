import re
import json

# Charger dataset
with open("data/malagasy_roots.json", "r", encoding="utf-8") as f:
    data = json.load(f)

WORD_TO_ROOT = {}
ROOT_SET = set()

for entry in data:
    root = entry["racine"]
    ROOT_SET.add(root)
    WORD_TO_ROOT[root] = root
    for w in entry["derives"]:
        WORD_TO_ROOT[w] = root

PREFIXES = sorted([
    "a","an","bo","da","do",
    "f","fa","fan","fi","fo",
    "ga","go","ha","ho",
    "i","in","ja","jo",
    "k","ka","ki","ki2","ko",
    "la",
    "m","ma","man","mi","mo",
    "mp","mpa","mpi",
    "na",
    "pa","po",
    "ro",
    "sa","san","so",
    "t","ta","tan","to",
    "tsa","tsi","tsi2","tso",
    "va","vo","voa",
    "za",

    "faha","maha","mpaha",
    "fampa","mampa","mpampa",
    "fampan","mampan","mpampan",
    "fampi","mampi","mpampi",
    "fampo","mampo","mpampo",

    "fana","mana","mpana",
    "fanka","manka","mpanka",
    "fian","mian","mpian",

    "fifamp","mifamp","mpifamp",
    "fifan","mifan","mpifan",
    "fiha","miha","mpiha",

    "ampaha","fampaha","mampaha","mpampaha",
    "mampampa","mpampampa",
    "fampampi","mampampi","mpampampi",
    "fampana","mampana","mpampana",
    "fampanka","mampanka","mpampanka",
    "mampiha","mpampiha",
    "mampifan",
    "fifampa","mifampa","mpifampa",
    "fifampan","mifampan",
    "fifampi","mifampi","mpifampi",
    "fifana","mifana","mpifana",
    "fifanka","mifanka","mpifanka",
    "mampifampan",
    "mampifampi",
    "mampifana",
    "mampifanka",

    "kara","mango","soma","tafa","tako","tala"
], key=len, reverse=True)

SUFFIXES = ["ana", "ina", "na"]

# Alternances phonétiques connues (exemple: man + t -> n)
NASAL_ALTERNATIONS = {
    r'^man([td])': r'n\1',   # manosy -> nosy
    r'^mam([bp])': r'm\1',   # mamita -> mita
    r'^man([kgh])': r'n\1',
}

class MalagasyLemmatizer:

    # --- CHARGEMENT SÉCURISÉ ---
    for entry in data:
        root = entry["racine"]
        ROOT_SET.add(root)
        # On n'ajoute dans le dictionnaire de mapping que si ce n'est pas déjà une racine
        if root not in WORD_TO_ROOT:
            WORD_TO_ROOT[root] = root
        
        for w in entry["derives"]:
            # PRIORITÉ : Si le mot dérivé est déjà enregistré comme une RACINE, 
            # on ne l'écrase pas.
            if w not in ROOT_SET:
                WORD_TO_ROOT[w] = root
    
    # --- MÉTHODE LEMMATIZE ---
    def lemmatize(self, word: str) -> str:
        word = word.lower().strip()

        # 1. Si c'est déjà une racine connue, on s'arrête immédiatement !
        if word in ROOT_SET:
            return word
    
        # 2. Si c'est un dérivé direct connu
        if word in WORD_TO_ROOT:
            return WORD_TO_ROOT[word]

        root = word

        # ✅ 2 suffix
        for s in SUFFIXES:
            if root.endswith(s) and len(root) > len(s)+2:
                root = root[:-len(s)]
                break

        # ✅ 3 prefix
        for p in PREFIXES:
            if root.startswith(p) and len(root) > len(p)+2:
                root = root[len(p):]
                break

        # ✅ 4 fallback dictionnaire
        if root in WORD_TO_ROOT:
            return WORD_TO_ROOT[root]

        # ✅ 5 fallback racine connue
        if root in ROOT_SET:
            return root

        return word

    def get_analysis(self, word: str) -> dict:
        root = self.lemmatize(word)
        return {"original": word, "root": root, "changed": root != word}