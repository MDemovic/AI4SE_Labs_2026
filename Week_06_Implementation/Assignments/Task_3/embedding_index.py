"""Build and query a local TF-IDF index for the Task 2 chunks."""
import argparse
import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

HERE = Path(__file__).resolve().parent
CHUNKS = HERE.parent / "Task_2" / "chunks.json"
INDEX = HERE / "chunk_index.joblib"


def build_index():
    chunks = json.loads(CHUNKS.read_text(encoding="utf-8-sig"))
    if not chunks:
        raise ValueError("The chunk file is empty; run Task 2's chunking script first.")
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([chunk["text"] for chunk in chunks])
    joblib.dump({"chunks": chunks, "vectors": vectors, "vectorizer": vectorizer}, INDEX, compress=3)
    print(f"Saved {len(chunks)} chunk-vector pairs with {vectors.shape[1]} dimensions to {INDEX}")


def search(query, limit):
    if limit < 1:
        raise ValueError("The number of results must be positive.")
    index = joblib.load(INDEX)
    query_vector = index["vectorizer"].transform([query])
    if query_vector.nnz == 0:
        print("No matching vocabulary in the query.")
        return
    scores = (index["vectors"] @ query_vector.T).toarray().ravel()
    ranked = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    for i in ranked[:limit]:
        if scores[i] <= 0:
            break
        chunk = index["chunks"][i]
        print(f"\n{chunk['path']}:{chunk['start_line']}-{chunk['end_line']} (score {scores[i]:.3f})")
        print(chunk["text"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="Rebuild the index after changing chunks")
    query = sub.add_parser("search", help="Find chunks for a coding task")
    query.add_argument("query")
    query.add_argument("-n", type=int, default=3)
    args = parser.parse_args()
    if args.command == "build":
        build_index()
    else:
        search(args.query, args.n)


if __name__ == "__main__":
    main()
