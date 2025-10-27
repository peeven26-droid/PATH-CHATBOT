from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client using API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Homepage route
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot API route
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # Load handbook content (only once at runtime)
    with open("handbook.txt", "r", encoding="utf-8") as f:
        handbook_text = f.read()

    # Create a prompt that limits the chatbot strictly to the handbook
    system_prompt = (
        "You are PATH, a helpful student handbook assistant for St. Mary’s College of Baliuag. "
        "Answer ONLY based on the information provided in the handbook text below. "
        "If the question is not related to the handbook, reply with: "
        "'Sorry, I cannot answer that for you. Would you like to ask another question?'\n\n"
        f"Handbook content:\n{handbook_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

