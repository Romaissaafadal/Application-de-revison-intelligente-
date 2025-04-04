import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ProjetSD"]
collection = db["FichesRevision"]

def show():
    st.title("📚 Fiches de Révision")

    docs = list(collection.find())
    for doc in docs:
        with st.expander(f"📌 {doc['title']}"):
            st.write(f"**Mots-clés:** {', '.join(doc['keywords'])}")
            st.write(f"**Résumé:** {doc['summary']}")

