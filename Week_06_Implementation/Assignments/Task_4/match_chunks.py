import argparse
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

INDEX = Path(__file__).resolve().parent.parent / "Task_3" / "chunk_index.joblib"


def match_embeddings(index, task_embedding, n=5):
    """Return up to n chunk/score pairs, sorted by cosine similarity."""
    if n < 1:
        raise ValueError("n must be positive")
    if task_embedding.shape != (1, index["vectors"].shape[1]):
        raise ValueError("Expected one task embedding with the same dimensions as the index")
    if task_embedding.nnz == 0:
        return []
    scores = cosine_similarity(task_embedding, index["vectors"])[0]
    ranked = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
    return [(index["chunks"][i], float(scores[i])) for i in ranked[:n]]


def find_chunks(index, task, n=5):
    """Embed a textual task with the index's fitted vocabulary and find matches."""
    return match_embeddings(index, index["vectorizer"].transform([task]), n)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", help="Coding task to search for")
    parser.add_argument("-n", type=int, default=5, help="Maximum number of chunks (default: 5)")
    args = parser.parse_args()
    index = joblib.load(INDEX)
    matches = find_chunks(index, args.task, args.n)
    if not matches:
        print("The task has no words in the index vocabulary; no matches found.")
    for chunk, score in matches:
        print(f"\n{chunk['path']}:{chunk['start_line']}-{chunk['end_line']} (score {score:.3f})")
        print(chunk["text"])


if __name__ == "__main__":
    main()

