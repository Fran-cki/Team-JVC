import re

# Préfixes et suffixes Malagasy (annexe du sujet + linguistique MG)
PREFIXES = [
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
]

SUFFIXES = ["-ana", "-ina", "-na"]

# Alternances phonétiques connues (exemple: man + t -> n)
NASAL_ALTERNATIONS = {
    r'^man([td])': r'n\1',   # manosy -> nosy
    r'^mam([bp])': r'm\1',   # mamita -> mita
    r'^man([kgh])': r'n\1',
}

class MalagasyLemmatizer:
    def lemmatize(self, word: str) -> str:
        word = word.lower().strip()
        root = word

        # Étape 1 : retirer les suffixes
        for suffix in SUFFIXES:
            clean = suffix.lstrip("-")
            if root.endswith(clean) and len(root) > len(clean) + 3:
                root = root[: -len(clean)]
                break

        # Étape 2 : retirer les préfixes (du plus long au plus court)
        for prefix in sorted(PREFIXES, key=len, reverse=True):
            if root.startswith(prefix) and len(root) > len(prefix) + 2:
                root = root[len(prefix):]
                break

        # Étape 3 : alternances nasales
        for pattern, replacement in NASAL_ALTERNATIONS.items():
            root = re.sub(pattern, replacement, root)

        return root if root else word

    def get_analysis(self, word: str) -> dict:
        root = self.lemmatize(word)
        return {"original": word, "root": root, "changed": root != word}