"""Evaluate Task 2 SQL by restaurant-name overlap, preserving duplicates.

Run from any directory: python path/to/evaluate_name_metrics.py
Uses the supplied database loader; never changes predictions or reference labels.
"""

import csv
import importlib.util
import json
import sqlite3
from collections import Counter
from pathlib import Path


TASK3 = Path(__file__).resolve().parent
TASK2 = TASK3.parent / "Task_2"
DATA = TASK2 / "data"


def name_metrics(expected_names, predicted_names):
    """Return multiset precision, recall, F1, and exact-match status.

    Both empty: all scores are 1. Only one empty: all scores are 0.
    Otherwise TP is the sum of minimum expected/predicted name counts.
    Names are compared exactly as stored, without fuzzy matching or case folding.
    """
    expected = Counter(expected_names)
    predicted = Counter(predicted_names)
    if not expected and not predicted:
        return 1.0, 1.0, 1.0, True
    if not expected or not predicted:
        return 0.0, 0.0, 0.0, False
    true_positive = sum((expected & predicted).values())
    expected_count = sum(expected.values())
    predicted_count = sum(predicted.values())
    return (
        true_positive / predicted_count,
        true_positive / expected_count,
        2 * true_positive / (expected_count + predicted_count),
        expected == predicted,
    )


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        return reader.fieldnames, list(reader)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    csv.field_size_limit(1_000_000_000)
    spec = importlib.util.spec_from_file_location(
        "original_evaluator", DATA / "evaluate_retrieval_predictions.py"
    )
    evaluator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evaluator)
    _, labels = read_csv(DATA / "restaurants_dataset.csv")
    if not labels:
        raise ValueError("No reference questions found")
    expected_results = [json.loads(row["result"]) for row in labels]
    if any(
        not isinstance(rows, list)
        or any(not isinstance(row, list) or len(row) != 2 for row in rows)
        for rows in expected_results
    ):
        raise ValueError("Expected labels containing [ID, NAME] rows")

    connection = evaluator.load_database()
    connection.execute("PRAGMA query_only = ON")
    details = []
    summaries = []
    try:
        for framework in ("ICIO", "REACT", "SCOPE"):
            header, predictions = read_csv(
                TASK2 / framework / "restaurants_dataset_predictions.csv"
            )
            if header != ["question", "predicted_sql"]:
                raise ValueError(f"Invalid CSV header for {framework}")
            if [row["question"] for row in predictions] != [
                row["question"] for row in labels
            ]:
                raise ValueError(f"Questions missing, changed, or reordered: {framework}")

            framework_details = []
            for index, (prediction, expected) in enumerate(
                zip(predictions, expected_results), start=1
            ):
                error = ""
                predicted = []
                try:
                    cursor = connection.execute(prediction["predicted_sql"])
                    if cursor.description is None:
                        raise ValueError("Query must return a result set")
                    predicted = cursor.fetchall()
                    # Empty results contain no names to extract. As in the original
                    # evaluator, empty/empty matches regardless of projected columns.
                    predicted_names = []
                    if predicted:
                        name_columns = [
                            i for i, column in enumerate(cursor.description)
                            if column[0].upper() == "NAME"
                        ]
                        if len(name_columns) != 1:
                            raise ValueError("Nonempty output must contain one NAME column")
                        predicted_names = [row[name_columns[0]] for row in predicted]
                        if any(not isinstance(name, str) for name in predicted_names):
                            raise ValueError("NAME column must contain strings")
                    precision, recall, f1, exact = name_metrics(
                        [row[1] for row in expected], predicted_names
                    )
                except (sqlite3.Error, ValueError) as exception:
                    # An invalid query always fails, even if expected rows are empty.
                    error = str(exception)
                    precision = recall = f1 = 0.0
                    exact = False

                detail = {
                    "framework": framework,
                    "question_index": index,
                    "question": prediction["question"],
                    "expected_count": len(expected),
                    "predicted_count": len(predicted),
                    "original_exact": int(
                        not error
                        and Counter(predicted) == Counter(tuple(row) for row in expected)
                    ),
                    "name_exact": int(exact),
                    "name_precision": precision,
                    "name_recall": recall,
                    "name_f1": f1,
                    "error": error,
                }
                framework_details.append(detail)
                details.append(detail)

            count = len(framework_details)
            nonempty = [row for row in framework_details if row["expected_count"]]
            summary = {
                "framework": framework,
                "question_count": count,
                "execution_errors": sum(bool(row["error"]) for row in framework_details),
                "original_correct": sum(row["original_exact"] for row in framework_details),
                "original_accuracy": sum(row["original_exact"] for row in framework_details) / count,
                "name_exact_correct": sum(row["name_exact"] for row in framework_details),
                "name_exact_accuracy": sum(row["name_exact"] for row in framework_details) / count,
                "macro_name_precision": sum(row["name_precision"] for row in framework_details) / count,
                "macro_name_recall": sum(row["name_recall"] for row in framework_details) / count,
                "macro_name_f1": sum(row["name_f1"] for row in framework_details) / count,
                "nonempty_question_count": len(nonempty),
                "nonempty_macro_name_f1": (
                    sum(row["name_f1"] for row in nonempty) / len(nonempty)
                    if nonempty else ""
                ),
            }
            summaries.append(summary)
            print(
                f"{framework}: name F1={summary['macro_name_f1']:.6%}; "
                f"name exact={summary['name_exact_correct']}/{count}; "
                f"original={summary['original_correct']}/{count}; "
                f"errors={summary['execution_errors']}"
            )
    finally:
        connection.close()

    write_csv(TASK3 / "name_metrics_per_question.csv", details)
    write_csv(TASK3 / "name_metrics_summary.csv", summaries)
    print("Saved name_metrics_per_question.csv and name_metrics_summary.csv")


if __name__ == "__main__":
    main()
