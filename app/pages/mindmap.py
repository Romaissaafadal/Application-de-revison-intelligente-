import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from app.database.mango_connection import get_db

db=get_db()
collection = db["FichesRevision"]


def generate_mindmap(title, keywords, entities):
    G = nx.Graph()
    G.add_node(title, color='red', size=800)

    for kw in keywords:
        G.add_node(kw, color='blue', size=500)
        G.add_edge(title, kw)

    for entity in entities:
        G.add_node(entity, color='green', size=500)
        G.add_edge(title, entity)

    pos = nx.spring_layout(G)
    colors = [G.nodes[n]["color"] for n in G.nodes]
    sizes = [G.nodes[n]["size"] for n in G.nodes]

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=10, font_weight='bold')
    st.pyplot(plt)


def show():
    st.title("🧠 Cartes Mentales")

    docs = list(collection.find())
    for doc in docs:
        if st.button(f"Générer la carte mentale de {doc['title']}"):
            generate_mindmap(doc['title'], doc['keywords'], doc['named_entities'].keys())
