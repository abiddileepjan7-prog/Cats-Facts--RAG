from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from rag import generate_answer


BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/styles.css")
def styles():
    return send_from_directory(BASE_DIR, "styles.css")


@app.get("/app.js")
def script():
    return send_from_directory(BASE_DIR, "app.js")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()

    if not query:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        result = generate_answer(query)
    except Exception as exc:
        return jsonify({"error": f"Chatbot error: {exc}"}), 500

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
