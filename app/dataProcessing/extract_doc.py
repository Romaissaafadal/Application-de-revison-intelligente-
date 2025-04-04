import os
import fitz  # PyMuPDF
from docx import Document
from pptx import Presentation
from pymongo import MongoClient
from datetime import datetime

# ---------------------------
# 1. Configuration initiale
# ---------------------------

# Dossier contenant les fichiers
BASE_DIR = r"C:\Users\Romaissae\OneDrive\Documents\Wondershare\Wondershare Filmora\Output\Nouveau dossier\sd_docs_2\sd_docs\laravel"
FORMATS = ["pdf", "docx", "pptx"]  # Formats acceptés

# Connexion MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ProjetSD"]
    collection = db["Laravel"]
    client.admin.command('ping')  # Vérifier la connexion
    print("✅ Connexion MongoDB réussie")
except Exception as e:
    print(f"❌ Erreur de connexion MongoDB : {str(e)}")
    exit()


# ---------------------------
# 2. Fonctions d'extraction
# ---------------------------

def extract_pdf_text(file_path):
    """Extrait le texte d'un PDF avec PyMuPDF"""
    try:
        doc = fitz.open(file_path)
        return " ".join([page.get_text() for page in doc])
    except Exception as e:
        print(f"❌ Erreur extraction PDF {file_path} : {str(e)}")
        return ""


def extract_docx_text(file_path):
    """Extrait le texte d'un DOCX avec python-docx"""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"❌ Erreur extraction DOCX {file_path} : {str(e)}")
        return ""


def extract_pptx_text(file_path):
    """Extrait le texte d'un PPTX avec python-pptx"""
    try:
        prs = Presentation(file_path)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return "\n".join(text)
    except Exception as e:
        print(f"❌ Erreur extraction PPTX {file_path} : {str(e)}")
        return ""


# ---------------------------
# 3. Parcours des fichiers
# ---------------------------

inserted_count = 0  # Compteur des fichiers insérés

for filename in os.listdir(BASE_DIR):  # Liste tous les fichiers du dossier
    file_path = os.path.join(BASE_DIR, filename)

    # Vérifie si c'est un fichier et s'il a une extension supportée
    if not os.path.isfile(file_path) or not filename.lower().endswith(tuple(FORMATS)):
        continue  # Ignore les fichiers non valides

    print(f"✅ Fichier trouvé : {filename}")  # Vérification

    # Extraction du texte selon le format
    try:
        if filename.endswith(".pdf"):
            content = extract_pdf_text(file_path)
        elif filename.endswith(".docx"):
            content = extract_docx_text(file_path)
        elif filename.endswith(".pptx"):
            content = extract_pptx_text(file_path)

        if not content.strip():
            print(f"⚠ Fichier vide ou erreur d'extraction : {filename}")
            continue
        else:
            print(f"✅ Extraction réussie pour : {filename}")
    except Exception as e:
        print(f"❌ Erreur avec {filename}: {str(e)}")
        continue

    # Structure des données à insérer
    document = {
        "title": filename,
        "content": content,
        "file_type": filename.split('.')[-1],
        "source": "Université XYZ",
        "extracted_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Insertion dans MongoDB
    collection.insert_one(document)
    inserted_count += 1  # Incrémentation du compteur

print(f"📌 {inserted_count} cours insérés dans MongoDB !")

# ---------------------------
# 4. Vérification
# ---------------------------

if inserted_count > 0:
    print("\n📌 Affichage de 3 documents insérés :")
    for doc in collection.find().limit(3):
        print(f"\n--- {doc['title']} ---")
        print(doc["content"][:200] + "...")  # Affiche les 200 premiers caractères
else:
    print("⚠ Aucun document inséré, vérifie les logs ci-dessus.")
