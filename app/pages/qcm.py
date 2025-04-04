import streamlit as st
from app.database.mango_connection import get_db

db=get_db()
collection = db["QCM"]

def show():
    st.title("✅ QCM Interactif")

    docs = list(collection.find())
    for doc in docs:
        st.subheader(f"📖 {doc['title']}")
        for q in doc["questions"]:
            user_answer = st.radio(q["question"], q["options"], key=q["question"])
            if st.button(f"Vérifier {q['question']}"):
                if user_answer == q["correct_answer"]:
                    st.success("✅ Bonne réponse !")
                else:
                    st.error(f"❌ Mauvaise réponse. Réponse correcte : {q['correct_answer']}")
