import re
import string
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords

# Télécharger les stopwords français si nécessaire
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("french"))

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ProjetSD"]

# Liste des collections (modules)
modules = ["Laravel", "Module2", "Module3", "Module4", "Module5", "Module6", "Module7",
           "Module8"]  # Remplace avec les vrais noms


def clean_text(text):
    """Nettoie le texte en supprimant les éléments inutiles et en le structurant."""

    # 1. Supprimer les espaces et sauts de ligne inutiles
    text = re.sub(r'\s+', ' ', text).strip()

    # 2. Supprimer les caractères spéciaux (sauf la ponctuation utile)
    text = re.sub(r'[^\w\s.,;!?-]', '', text)

    # 3. Convertir en minuscule sauf les titres (phrases commençant par majuscule)
    text = ". ".join([sent.capitalize() for sent in text.split(". ")])

    # 4. Supprimer les stopwords
    words = text.split()
    text = " ".join([word for word in words if word.lower() not in STOPWORDS])

    return text


# Parcourir toutes les collections (modules)
for module in modules:
    collection = db[module]
    documents = collection.find()

    for doc in documents:
        text = doc["content"]

        # Nettoyer le texte
        cleaned_text = clean_text(text)

        # Mettre à jour MongoDB
        collection.update_one({"_id": doc["_id"]}, {"$set": {"cleaned_content": cleaned_text}})
        print(f"✅ Texte nettoyé pour {doc['title']} dans {module}")

print("🚀 Nettoyage terminé ! Toutes les collections ont été mises à jour.")
