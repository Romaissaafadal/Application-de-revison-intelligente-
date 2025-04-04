import networkx as nx
import matplotlib.pyplot as plt
from app.database.mango_connection import get_db

# Connexion MongoDB
db=get_db()
collection = db["FichesRevision"]

def generate_mindmap(doc):
    """Crée un schéma de carte mentale basé sur les mots-clés et les entités nommées"""
    title = doc["title"]
    keywords = doc["keywords"]
    entities = list(doc["named_entities"].keys())

    G = nx.Graph()
    G.add_node(title, color='red', size=800)  # Titre principal en rouge

    for kw in keywords:
        G.add_node(kw, color='blue', size=500)
        G.add_edge(title, kw)

    for entity in entities:
        G.add_node(entity, color='green', size=500)
        G.add_edge(title, entity)

    # Dessin du graphe
    pos = nx.spring_layout(G)
    colors = [G.nodes[n]["color"] for n in G.nodes]
    sizes = [G.nodes[n]["size"] for n in G.nodes]

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=10, font_weight='bold')
    plt.title(f"Carte mentale : {title}")
    plt.show()

# Génération des cartes mentales pour les fiches de révision
for doc in collection.find().limit(3):  # On limite pour tester
    generate_mindmap(doc)
