import spacy
import re
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer

# Charger le modèle NLP français de spaCy
nlp = spacy.load("fr_core_news_md")

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ProjetSD"]

# Liste des collections (modules)
modules = ["BaseDonnées", "DevelopementMobile", "java", "Laravel", "Programmation_js", "Programmation_mobile_js", "ProgrammationWeb",
           "php"]


def extract_titles(text):
    """Détecte les titres et sous-titres en repérant les lignes en majuscules ou longues."""
    lines = text.split(". ")  # On divise le texte en phrases
    titles = [line.strip() for line in lines if line.isupper() or len(line) > 50]
    return titles


def extract_keywords(text, num_keywords=10):
    """Extrait les mots-clés les plus importants avec TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words="french", max_features=num_keywords)
    X = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return list(keywords)


def extract_named_entities(text):
    """Extrait les entités nommées (noms propres, organisations, lieux...) avec spaCy."""
    doc = nlp(text)
    entities = {ent.text: ent.label_ for ent in doc.ents}
    return entities


# Parcourir toutes les collections (modules)
for module in modules:
    collection = db[module]
    documents = collection.find()

    for doc in documents:
        text = doc["cleaned_content"]  # Utiliser le texte nettoyé

        # Extraction des informations
        titles = extract_titles(text)
        keywords = extract_keywords(text)
        entities = extract_named_entities(text)

        # Mise à jour MongoDB
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {
                "titles": titles,
                "keywords": keywords,
                "named_entities": entities
            }}
        )
        print(f"✅ Extraction terminée pour {doc['title']} dans {module}")

print("🚀 Extraction des concepts clés terminée pour tous les modules !")
