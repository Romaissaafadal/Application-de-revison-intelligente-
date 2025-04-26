import matplotlib.pyplot as plt
import networkx as nx

def generer_carte_mentale(graphe, nom_fichier):
    G = nx.Graph()
    for lien in graphe:
        G.add_edge(lien["source"], lien["cible"], weight=lien["poids"])
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, node_size=1500, edge_color='gray')
    plt.title("Carte mentale - concepts clés")
    plt.savefig(nom_fichier)
    plt.close()
