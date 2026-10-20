"""Turn .txt, .md, and .eml files into one reviewed requirements document.
Set OPENAI_API_KEY, then run:
    python requirements_network.py --input-dir path/to/corpus --output requirements.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

EXTRACT_MODEL = "gpt-4o-mini"
CONSOLIDATE_MODEL = "gpt-5-mini"
REVIEW_MODEL = "gpt-4.1-nano"
MAX_REVISIONS = 2


class State(TypedDict, total=False):
    input_dir: str
    output_file: str
    documents: list[dict[str, str]]
    candidates: list[dict[str, Any]]
    requirements: list[dict[str, Any]]
    blacklist: list[dict[str, Any]]
    open_questions: list[Any]
    review: dict[str, Any]
    revision_count: int


def model_reply(model_name: str, prompt: str) -> dict[str, Any]:
    """Call a model and parse its JSON object response."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before running this script.")
    response = ChatOpenAI(model=model_name).invoke(prompt)
    content = response.content
    if isinstance(content, list):
        content = "\n".join(x.get("text", "") if isinstance(x, dict) else str(x) for x in content)
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", str(content).strip(), flags=re.I)
    start = text.find("{")
    if start < 0:
        raise ValueError(f"Model did not return JSON: {text[:250]}")
    result, _ = json.JSONDecoder().raw_decode(text[start:])
    if not isinstance(result, dict):
        raise ValueError("Expected a JSON object from the model.")
    return result


def read_email(path: Path) -> str:
    """Read an email's subject and text body, skipping attachments."""
    message = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
    parts = [f"Subject: {message['subject']}"] if message.get("subject") else []
    body_parts = message.walk() if message.is_multipart() else [message]
    for part in body_parts:
        if part.get_content_disposition() == "attachment":
            continue
        if part.get_content_type() not in {"text/plain", "text/html"}:
            continue
        try:
            body = part.get_content()
        except (LookupError, UnicodeError):
            continue
        if part.get_content_type() == "text/html":
            body = re.sub(r"<[^>]+>", " ", body)
            body = re.sub(r"\s+", " ", body)
        if body.strip():
            parts.append(body.strip())
            if part.get_content_type() == "text/plain":
                break
    return "\n\n".join(parts)


def load_documents(state: State) -> dict[str, Any]:
    root = Path(state["input_dir"]).expanduser().resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Input folder does not exist: {root}")
    paths = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md", ".eml"})
    if not paths:
        raise FileNotFoundError(f"No .txt, .md, or .eml files found in {root}")

    documents = []
    for i, path in enumerate(paths, 1):
        content = read_email(path) if path.suffix.lower() == ".eml" else path.read_text(encoding="utf-8", errors="replace")
        documents.append({
            "source_id": f"DOC-{i:03d}",
            "filename": str(path.relative_to(root)),
            "text": content.strip(),
        })
    print(f"Read {len(documents)} documents from {root}")
    return {"documents": documents}


def extract_candidates(state: State) -> dict[str, Any]:
    candidates = []
    for doc in state["documents"]:
        prompt = f'''Find every distinct, plausible software requirement in this document.
        Keep one behavior or constraint per candidate. Do not invent details. Include a short
        exact quote as evidence. Preserve unclear statements and mark uncertain=true.
        Return only JSON: {{"candidates":[{{"name":"short label","statement":"requirement",
        "evidence":"exact quote","uncertain":false}}]}}
        Source ID: {doc['source_id']}
        Filename: {doc['filename']}
        Document:
        {doc['text']}'''
        result = model_reply(EXTRACT_MODEL, prompt)
        for item in result.get("candidates", []):
            if isinstance(item, dict) and item.get("statement"):
                candidates.append({
                    "candidate_id": f"CAND-{len(candidates) + 1:04d}",
                    "source_id": doc["source_id"],
                    "filename": doc["filename"],
                    "name": str(item.get("name", "Unlabelled")),
                    "statement": str(item["statement"]),
                    "evidence": str(item.get("evidence", "")),
                    "uncertain": bool(item.get("uncertain", False)),
                })
    print(f"Extracted {len(candidates)} candidate requirements")
    return {"candidates": candidates}


def source_text(documents: list[dict[str, str]]) -> str:
    return json.dumps(documents, ensure_ascii=False)


def consolidate(state: State) -> dict[str, Any]:
    """AI node 2: merge duplicates, standardize wording, set priority, note conflicts."""
    prompt = f'''Create a concise, consistent set of software requirements from these candidates.
Merge semantic duplicates; keep different behaviors separate; do not invent details.
Each requirement needs a short name, paragraph explanation, priority, and source IDs.
Use only Must, Should, Could. Must=essential; Should=important but not essential to a
reasonable first release; Could=optional. Priorities are estimates unless explicitly
stated by a source. Put nonsensical or explicitly rejected conflicting items in the
blacklist with a reason. For unresolved conflicts, keep both evidence and add an open
question instead of guessing.
Return only JSON: {{"requirements":[{{"name":"...","explanation":"...","priority":"Must",
"sources":["DOC-001"]}}],"blacklist":[{{"name":"...","reason":"...","sources":["DOC-001"]}}],
"open_questions":["..."]}}
Candidates:
{json.dumps(state['candidates'], ensure_ascii=False)}'''
    result = model_reply(CONSOLIDATE_MODEL, prompt)
    return {
        "requirements": result.get("requirements", []),
        "blacklist": result.get("blacklist", []),
        "open_questions": result.get("open_questions", []),
        "revision_count": 0,
    }


def review(state: State) -> dict[str, Any]:
    """AI node 3: compare the draft with all source texts and the candidate list."""
    prompt = f'''Check the draft against the source documents and candidate list.
Find missed requirements, duplicates, contradictions, unsupported claims, inconsistent
terms, missing source references, and items that need a blacklist entry or open question.
Be specific. Return only JSON: {{"passed":true,"issues":[]}}. Set passed=false for any
meaningful issue.
SOURCE DOCUMENTS:
{source_text(state['documents'])}
CANDIDATES:
{json.dumps(state['candidates'], ensure_ascii=False)}
DRAFT:
{json.dumps({"requirements": state["requirements"], "blacklist": state["blacklist"], "open_questions": state["open_questions"]}, ensure_ascii=False)}'''
    result = model_reply(REVIEW_MODEL, prompt)
    return {"review": {"passed": bool(result.get("passed", False)), "issues": result.get("issues", [])}}


def revise(state: State) -> dict[str, Any]:
    """AI node: fix the reviewer's issues, then send the draft around the loop again."""
    prompt = f'''Revise this requirements draft to fix the review issues. Preserve source IDs,
use consistent wording, merge duplicates, and do not invent details. Keep unresolved
conflicts in open_questions. Return only JSON with this shape:
{{"requirements":[{{"name":"...","explanation":"...","priority":"Must","sources":["DOC-001"]}}],
"blacklist":[{{"name":"...","reason":"...","sources":["DOC-001"]}}],"open_questions":["..."]}}
SOURCE DOCUMENTS:
{source_text(state['documents'])}
CANDIDATES:
{json.dumps(state['candidates'], ensure_ascii=False)}
REVIEW ISSUES:
{json.dumps(state['review'].get('issues', []), ensure_ascii=False)}
DRAFT:
{json.dumps({"requirements": state["requirements"], "blacklist": state["blacklist"], "open_questions": state["open_questions"]}, ensure_ascii=False)}'''
    result = model_reply(CONSOLIDATE_MODEL, prompt)
    return {
        "requirements": result.get("requirements", []),
        "blacklist": result.get("blacklist", []),
        "open_questions": result.get("open_questions", []),
        "revision_count": state.get("revision_count", 0) + 1,
    }


def route_review(state: State) -> str:
    if state["review"].get("passed") or state.get("revision_count", 0) >= MAX_REVISIONS:
        return "render"
    return "revise"


def render(state: State) -> dict[str, Any]:
    """Deterministic node: assign IDs, check sources/priorities, and write Markdown."""
    valid_sources = {doc["source_id"] for doc in state["documents"]}
    source_names = {doc["source_id"]: doc["filename"] for doc in state["documents"]}
    lines = [
        "# Refined Software Requirements", "",
        "## Priority scale", "",
        "- **Must:** Essential for the system's core needs.",
        "- **Should:** Important, but a reasonable first release can work without it.",
        "- **Could:** Useful but optional.",
        "- Priorities are estimates unless a source explicitly states them.", "",
        "## Requirements", "",
    ]
    warnings = []
    requirements = [r for r in state.get("requirements", []) if isinstance(r, dict)]
    if not requirements:
        lines.extend(["No requirements were returned. Review the run and its inputs.", ""])
    for i, req in enumerate(requirements, 1):
        sources = [str(s) for s in req.get("sources", []) if str(s) in valid_sources]
        if not sources:
            warnings.append(f"No valid source recorded for {req.get('name', 'unnamed requirement')}.")
        priority = str(req.get("priority", "Should")).capitalize()
        if priority not in {"Must", "Should", "Could"}:
            warnings.append(f"Invalid priority for {req.get('name', 'unnamed requirement')}; changed to Should.")
            priority = "Should"
        lines.extend([
            f"### REQ-{i:03d} — {req.get('name', 'Unnamed requirement')}", "",
            str(req.get("explanation", "Explanation not supplied.")), "",
            f"**Priority:** {priority}  ",
            f"**Sources:** {', '.join(sources) if sources else 'No source recorded'}", "",
        ])

    lines.extend(["## Blacklisted requirements", ""])
    blacklist = [x for x in state.get("blacklist", []) if isinstance(x, dict)]
    if not blacklist:
        lines.extend(["No requirements were discarded.", ""])
    for item in blacklist:
        refs = ", ".join(map(str, item.get("sources", []))) or "No source recorded"
        lines.append(f"- **{item.get('name', 'Unnamed item')}:** {item.get('reason', 'No reason supplied.')} (sources: {refs})")
    lines.extend(["", "## Open questions", ""])
    questions = state.get("open_questions", [])
    lines.extend([f"- {q}" for q in questions] if questions else ["None recorded."])
    lines.extend(["", "## Source documents", ""])
    lines.extend([f"- **{sid}:** `{filename}`" for sid, filename in source_names.items()])

    review_result = state.get("review", {})
    if not review_result.get("passed"):
        lines.extend(["", "## Review notes", "", "The draft still had review issues after the retry limit."])
        lines.extend(f"- {issue}" for issue in review_result.get("issues", []))
    if warnings:
        lines.extend(["", "## Validation notes", ""])
        lines.extend(f"- {warning}" for warning in warnings)

    output = Path(state["output_file"]).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output}")
    return {}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("load", load_documents)
    graph.add_node("extract", extract_candidates)
    graph.add_node("consolidate", consolidate)
    graph.add_node("review", review)
    graph.add_node("revise", revise)
    graph.add_node("render", render)
    graph.set_entry_point("load")
    graph.add_edge("load", "extract")
    graph.add_edge("extract", "consolidate")
    graph.add_edge("consolidate", "review")
    graph.add_conditional_edges("review", route_review, {"revise": "revise", "render": "render"})
    graph.add_edge("revise", "review")
    graph.add_edge("render", END)
    return graph.compile()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", required=True, help="Folder containing .txt, .md, and .eml files")
    parser.add_argument("--output", default="requirements.md", help="Output Markdown file")
    args = parser.parse_args()
    build_graph().invoke({"input_dir": args.input_dir, "output_file": args.output})


if __name__ == "__main__":
    main()
