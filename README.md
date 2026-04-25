# 🐱 Cat Facts RAG Chatbot

A full-stack **Retrieval-Augmented Generation (RAG)** application that answers questions about cats using a local dataset, embeddings, and a lightweight web interface.

---

## 🚀 Features

* 📚 Uses a custom dataset of cat facts (`cat-facts.txt`)
* 🔍 Embedding-based semantic search with Ollama
* 🧠 Cosine similarity retrieval
* 💬 Context-aware answers using an LLM
* 🌐 Simple frontend (HTML/CSS/JS)
* ⚡ Fast and fully local (no external APIs required)

---

## 🛠️ Tech Stack

**Backend**

* Python
* NumPy
* Ollama (embeddings + LLM)

**Frontend**

* HTML
* CSS
* JavaScript

---

## 📂 Project Structure

```
CATS_FACTS_RAG/
└── Cats-Facts--RAG/
    ├── __pycache__/
    ├── .venv/              # Virtual environment
    ├── rag.py              # Core RAG pipeline
    ├── app.py              # Backend server
    ├── app.js              # Frontend logic
    ├── index.html          # UI
    ├── styles.css          # Styling
    ├── cat-facts.txt       # Dataset
    ├── requirements.txt    # Python dependencies
    ├── vercel.json         # Deployment config
    └── README.md
```

---

## ⚙️ How It Works

### 1. Data Loading

* Reads cat facts from `cat-facts.txt`
* Each line is treated as a separate knowledge chunk

### 2. Embedding

* Uses:

  ```
  nomic-embed-text
  ```
* Converts each chunk into a vector

### 3. Retrieval

* User query is embedded
* Cosine similarity is used to find top relevant chunks

### 4. Generation

* Uses:

  ```
  llama3
  ```
* The model is instructed to:

  * Only use retrieved context
  * Avoid hallucinations

---

## 🧪 Example

**Input:**

```
Why do cats purr?
```

**Retrieved Context:**

```
Cats purr for communication and self-soothing
Kittens purr to communicate with their mothers
```

**Output:**

```
Cats purr for communication and self-soothing, and kittens use purring to communicate with their mothers.
```

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/cats-facts-rag.git
cd cats-facts-rag
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Ollama

Download from: https://ollama.com/

Then run:

```bash
ollama pull nomic-embed-text
ollama pull llama3
```

---

## ▶️ Running the App

### Start backend

```bash
python app.py
```

### Open frontend

Open `index.html` in your browser
(or serve it using a local server)

---

## 📄 Dataset Format

`cat-facts.txt`

```
Cats sleep for 12–16 hours a day.
Cats have retractable claws.
A group of cats is called a clowder.
```

Each line = one knowledge chunk.

---

## ⚠️ Limitations

* In-memory vector database (not persistent)
* No batching or chunking for large documents
* Basic frontend (no streaming responses)
* Depends on local Ollama runtime

---

## 🔮 Future Improvements

* Replace in-memory DB with FAISS / Chroma
* Add API endpoints for better frontend integration
* Streaming responses
* Chat history memory
* Deploy full stack (Vercel + backend hosting)

---

## 📜 License

MIT License

---

## 🙌 Acknowledgements

* Ollama for local LLM + embeddings
* RAG architecture inspiration from open-source community

---

## 💡 Notes

This project is intentionally simple and educational — perfect for understanding how RAG works without heavy frameworks.

---
