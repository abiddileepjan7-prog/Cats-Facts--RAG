from pathlib import Path

import numpy as np
import ollama


EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3"
DATASET_PATH = Path(__file__).with_name("cat-facts.txt")

VECTOR_DB = []
_IS_INDEXED = False


def add_chunk_to_db(chunk):
    response = ollama.embed(model=EMBEDDING_MODEL, input=chunk)

    if "embedding" in response:
        embedding = response["embedding"]
    elif "embeddings" in response:
        embeddings = response["embeddings"]
        if not embeddings:
            raise ValueError("Empty embeddings list")
        embedding = embeddings[0] if isinstance(embeddings[0], list) else embeddings
    else:
        raise ValueError(f"Could not find embedding in response: {response}")

    embedding_np = np.array(embedding, dtype=np.float32)
    VECTOR_DB.append((chunk, embedding_np))


def cosine_similarity(a, b):
    a_np = np.array(a, dtype=np.float32)
    b_np = np.array(b, dtype=np.float32)

    dot_product = np.dot(a_np, b_np)
    norm_a = np.linalg.norm(a_np)
    norm_b = np.linalg.norm(b_np)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def retrieve(query, top_n=3):
    response = ollama.embed(model=EMBEDDING_MODEL, input=query)

    if "embedding" in response:
        query_embedding = response["embedding"]
    elif "embeddings" in response:
        embeddings = response["embeddings"]
        if not embeddings:
            raise ValueError("Empty embeddings list")
        query_embedding = embeddings[0] if isinstance(embeddings[0], list) else embeddings
    else:
        raise ValueError(f"Unexpected query structure: {response}")

    query_embedding_np = np.array(query_embedding, dtype=np.float32)
    similarities = []

    for chunk, embedding_np in VECTOR_DB:
        similarity = cosine_similarity(query_embedding_np, embedding_np)
        similarities.append((chunk, similarity))

    similarities.sort(key=lambda item: item[1], reverse=True)
    return similarities[:top_n]


def load_dataset(dataset_path=DATASET_PATH):
    with Path(dataset_path).open("r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def ensure_indexed(dataset_path=DATASET_PATH):
    global _IS_INDEXED

    if _IS_INDEXED:
        return

    VECTOR_DB.clear()
    dataset = load_dataset(dataset_path)

    for chunk in dataset:
        add_chunk_to_db(chunk)

    _IS_INDEXED = True


def build_instruction_prompt(context_text):
    return (
        "You are a helpful chatbot that knows about cats. "
        "Use only the following context to answer the question. "
        "Do not make up any new information.\n\n"
        f"Context:\n{context_text}"
    )


def generate_answer(query, top_n=3):
    ensure_indexed()
    retrieved_knowledge = retrieve(query, top_n=top_n)

    context_text = "\n".join(chunk for chunk, _similarity in retrieved_knowledge)
    instruction_prompt = build_instruction_prompt(context_text)

    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {"role": "system", "content": instruction_prompt},
            {"role": "user", "content": query},
        ],
    )

    answer = response["message"]["content"].strip()
    matches = [
        {"text": chunk, "score": round(float(similarity), 4)}
        for chunk, similarity in retrieved_knowledge
    ]

    return {"answer": answer, "matches": matches}


def main():
    print("Loading dataset")
    dataset = load_dataset()
    print(f"Loaded {len(dataset)} entries")

    print("Indexing dataset")
    ensure_indexed()
    print("Index ready")

    while True:
        input_query = input("ASK ANY QUESTION ABOUT CATS: ").strip()
        if input_query.lower() == "exit":
            break

        print("Retrieving knowledge")
        result = generate_answer(input_query)
        print("Retrieved information")

        for match in result["matches"]:
            print(f"similarity: {match['score']:.2f} {match['text']}")

        print("Chatbot response")
        print(result["answer"])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("error occurred", e)
