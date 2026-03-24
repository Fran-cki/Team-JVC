from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Import des modules existants
from modules.spellchecker import MalagasySpellChecker
from modules.lemmatizer import MalagasyLemmatizer
from modules.phonotactics import MalagasyPhonotactics

# Import du nouveau moteur de prédiction
# Assure-toi d'avoir sauvegardé la classe MalagasyInferenceEngine dans modules/predictor.py
from modules.autocomplection import MalagasyInferenceEngine

app = FastAPI(title="Malagasy NLP API")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Initialisation des services
spell = MalagasySpellChecker()
lemma = MalagasyLemmatizer()
phono = MalagasyPhonotactics()

# Initialisation du moteur de prédiction (charge le JSON sauvegardé)
# Si le fichier n'existe pas encore, il faudra d'abord lancer l'entraînement
predictor = MalagasyInferenceEngine(model_path="data/model_ngram.json")

class TextRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

@app.post("/spell-check")
def spell_check(req: TextRequest):
    return {"errors": spell.check_text(req.text)}

@app.post("/lemmatize")
def lemmatize(req: TextRequest):
    words = req.text.split()
    return {"results": [lemma.get_analysis(w) for w in words]}

@app.post("/predict")
def predict_next_word(req: TextRequest):
    suggestions = predictor.predict(req.text, limit=5)
    return {"suggestions": suggestions}