from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os
app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Dein Chatbot</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 20px auto; }
    textarea { width: 100%; height: 120px; }
    #response { margin-top: 20px; white-space: pre-wrap; border: 1px solid #ccc; padding: 10px; }
    button { padding: 8px 16px; margin-top: 8px; }
  </style>
</head>
<body>
  <h1>Dein persönlicher Chatbot</h1>
  <p>Text hier einfügen, Bot antwortet passend. Nur für volljährige, einwilligende Chats verwenden.</p>
  <textarea id="msg" placeholder="Deine Nachricht…"></textarea><br>
  <button onclick="sendMsg()">Antwort holen</button>

  <div id="response"></div>

  <script>
    async function sendMsg() {
      const msg = document.getElementById("msg").value;
      const resDiv = document.getElementById("response");
      resDiv.innerText = "Lade Antwort...";
      const res = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
      });
      const data = await res.json();
      resDiv.innerText = data.response;
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    system_prompt = (
        "Du hilfst der Nutzerin, flirtende und erotische Antworten zu formulieren. "
        "Antworten nur für volljährige, einwilligende Personen, respektvoll und nicht beleidigend."
    )

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    )

    answer = completion.choices[0].message.content
    return jsonify({"response": answer})

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000)


