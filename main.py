from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

# Definition der relevanten Begriffe
PERSONENDATEN_KEYWORDS = [
    "Name", "Vorname", "Nachname", "Adresse", "E-Mail", "Telefonnummer",
    "Geburtsdatum", "AHV", "IP-Adresse", "Kundennummer", "Vertragsnummer"
]

VERARBEITUNG_KEYWORDS = [
    "erheben", "speichern", "verwenden", "analysieren", "verarbeiten", "übermitteln"
]

# Datenmodell für API-Anfragen
class VertragstextRequest(BaseModel):
    text: str

# API-Endpunkt für die Analyse
@app.post("/check-personendaten")
def check_personendaten(request: VertragstextRequest):
    text = request.text.lower()

    # Prüfen, ob relevante Begriffe vorkommen
    detected_terms = [
        term for term in PERSONENDATEN_KEYWORDS + VERARBEITUNG_KEYWORDS if re.search(r"\b" + term.lower() + r"\b", text)
    ]

    contains_personendaten = any(term in detected_terms for term in PERSONENDATEN_KEYWORDS) and any(
        term in detected_terms for term in VERARBEITUNG_KEYWORDS
    )

    return {
        "contains_personendaten": contains_personendaten,
        "detected_terms": detected_terms
    }
