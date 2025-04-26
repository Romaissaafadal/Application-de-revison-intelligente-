import pymongo
import re
import yake
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

#  modèle pour les embeddings
sbert_model = SentenceTransformer("allenai-specter")

# Connexion MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["ma_bdd_copie"]
col = db["documents"]


# Nettoyage du texte
def nettoyer_texte(texte):
    texte = re.sub(r"\s+", " ", texte)  # Supprime les espaces multiples
    texte = re.sub(r"[^\w\s]", "", texte)  # Supprime les caractères spéciaux
    texte = texte.lower()
    return texte.strip()


# Extraction des concepts avec YAKE
def extraire_concepts_yake(texte, top_k=30):
    kw_extractor = yake.KeywordExtractor(lan="fr", top=top_k)
    keywords = kw_extractor.extract_keywords(texte)
    return [kw for kw, _ in keywords]


# Génération des relations entre concepts
def generer_graphe_concepts(concepts):
    if len(concepts) < 2:
        return []

    embeddings = sbert_model.encode(concepts)
    sim = cosine_similarity(embeddings)

    G = nx.Graph()
    for i in range(len(concepts)):
        for j in range(i + 1, len(concepts)):
            if sim[i][j] > 0.5:
                G.add_edge(concepts[i], concepts[j], poids=float(sim[i][j]))

    return [{"source": u, "cible": v, "poids": d["poids"]} for u, v, d in G.edges(data=True)]


# Pipeline principal
def traiter_documents():
    documents = list(col.find())
    for doc in documents:
        texte_brut = doc.get("texte", "")
        if not texte_brut.strip():
            continue

        texte_nettoye = nettoyer_texte(texte_brut)
        print(f"\n🧹 Texte nettoyé (extrait): {texte_nettoye[:100]}...")  # DEBUG

        concepts = extraire_concepts_yake(texte_nettoye)
        print(f"🔍 Concepts extraits (YAKE) : {concepts}")  # DEBUG

        graphe = generer_graphe_concepts(concepts)

        col.update_one(
            {"_id": doc["_id"]},
            {"$set": {
                "texte_nettoye": texte_nettoye,
                "mots_cles": concepts,
                "graphe_concepts": graphe
            }}
        )
        print(f"✅ Document traité : {doc.get('nom', 'Sans nom')}")



if __name__ == "__main__":
    traiter_documents()

