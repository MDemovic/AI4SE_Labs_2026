import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent / "Task_1" / "AI4SE_Playground"
OUTPUT = HERE / "chunks.json"
CHUNK_LINES = 80
OVERLAP_LINES = 10
EXCLUDED = {".git", "__pycache__", ".venv", "venv", ".pytest_cache"}


def make_chunks(repository: Path) -> list[dict]:
    chunks = []
    for path in sorted(repository.rglob("*.py")):
        if any(part in EXCLUDED for part in path.relative_to(repository).parts):
            continue
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        start = 0
        while start < len(lines):
            end = min(start + CHUNK_LINES, len(lines))
            chunks.append({
                "path": path.relative_to(repository).as_posix(),
                "start_line": start + 1,
                "end_line": end,
                "text": "".join(lines[start:end]),
            })
            if end == len(lines):
                break
            start = end - OVERLAP_LINES
    return chunks


def main() -> None:
    if not REPOSITORY.is_dir():
        raise FileNotFoundError(f"Repository not found: {REPOSITORY}")
    chunks = make_chunks(REPOSITORY)
    OUTPUT.write_text(json.dumps(chunks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(chunks)} chunks to {OUTPUT}")


if __name__ == "__main__":
    main()
