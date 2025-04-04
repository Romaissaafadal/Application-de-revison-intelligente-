
import random
from app.database.mango_connection import get_db

db=get_db()
collection = db["FichesRevision"]
qcm_collection = db["QCM"]

for doc in collection.find():
    words = doc["summary"].split()
    questions = []
    for word in random.sample(words, min(3, len(words))):
        options = random.sample(words, 3) + [word]
        random.shuffle(options)
        questions.append({"question": f"Que signifie {word} ?", "options": options, "correct_answer": word})

    qcm_collection.insert_one({"title": doc["title"], "questions": questions})
