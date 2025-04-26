import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generer_qcm(texte, nb_questions=3):
    prompt = f"""Tu es un générateur de QCM. Génère {nb_questions} questions à choix multiples avec 4 choix chacun (A à D), une seule bonne réponse, à partir de ce texte :

{texte}

Formate-les en JSON, comme ceci :
[
  {{
    "question": "Quelle est la capitale de la France ?",
    "choix": ["A. Lyon", "B. Marseille", "C. Paris", "D. Lille"],
    "reponse": "C"
  }},
  ...
]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800,
        )

        # Extraire le contenu texte de la réponse
        contenu = response.choices[0].message["content"].strip()

        # Convertir la réponse JSON en objet Python
        import json
        qcm = json.loads(contenu)
        return qcm

    except Exception as e:
        print("⚠️ Erreur génération QCM :", e)
        return []
