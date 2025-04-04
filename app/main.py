import streamlit as st

st.set_page_config(page_title="Projet SD", layout="wide")

st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Aller à :", ["Fiches de Révision", "Cartes Mentales", "QCM"])

if page == "Fiches de Révision":
    from pages import revision
    revision.show()
elif page == "Cartes Mentales":
    from pages import mindmap
    mindmap.show()
elif page == "QCM":
    from pages import qcm
    qcm.show()
