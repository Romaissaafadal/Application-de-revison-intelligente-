import spacy

from transformers import pipeline
from app.database.mango_connection import get_db

# Charger le modèle de résumé BERT (Hugging Face)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Connexion MongoDB
db=get_db()

# Liste des collections (modules)
modules = ["Laravel", "Module2", "Module3", "Module4", "Module5", "Module6", "Module7", "Module8"]  # Remplace avec les vrais noms

def summarize_text(text, max_length=200):
    """Génère un résumé du texte avec BERT."""
    if len(text.split()) < 50:  # Trop court pour un résumé automatique
        return text
    return summarizer(text, max_length=max_length, min_length=50, do_sample=False)[0]["summary_text"]

# Parcourir toutes les collections (modules)
for module in modules:
    collection = db[module]
    documents = collection.find()

    for doc in documents:
        title = doc["title"]
        keywords = doc["keywords"]
        named_entities = doc["named_entities"]
        text = doc["cleaned_content"]

        # Générer un résumé intelligent
        summary = summarize_text(text)

        # Créer une fiche de révision
        fiche_revision = {
            "title": title,
            "keywords": keywords,
            "summary": summary,
            "named_entities": named_entities
        }

        # Stocker la fiche dans une nouvelle collection "FichesRevision"
        db["FichesRevision"].insert_one(fiche_revision)
        print(f"✅ Fiche de révision créée pour {title} dans {module}")

print("🚀 Génération des fiches de révision terminée !")
