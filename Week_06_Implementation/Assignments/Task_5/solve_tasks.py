import argparse
import ast
import importlib.util
import json
import os
from pathlib import Path
import textwrap

import joblib
from openai import OpenAI

HERE = Path(__file__).resolve().parent
ASSIGNMENTS = HERE.parent
REPOSITORY = ASSIGNMENTS / "Task_1" / "AI4SE_Playground"
TASKS = ASSIGNMENTS / "missing_code.json"
INDEX = ASSIGNMENTS / "Task_3" / "chunk_index.joblib"
MODELS = ("gpt-6-luna", "gpt-5.6-luna", "gpt-5.4-nano", "gpt-5-nano", "gpt-5-mini", "gpt-4.1-nano", "gpt-4o-mini")


def load_key():
    if os.environ.get("OPENAI_API_KEY"):
        return
    env_file = HERE / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8-sig").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == "OPENAI_API_KEY":
                os.environ["OPENAI_API_KEY"] = value.strip().strip("\"'")
                break
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("Add OPENAI_API_KEY to Task_5/.env or set the environment variable.")


def load_matcher():
    spec = importlib.util.spec_from_file_location("match_chunks", ASSIGNMENTS / "Task_4" / "match_chunks.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_chunks


def locate_method(source, class_name, method_name):
    tree = ast.parse(source)
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == class_name]
    if len(classes) != 1:
        raise ValueError(f"Expected one class named {class_name}")
    methods = [node for node in classes[0].body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method_name]
    if len(methods) != 1:
        raise ValueError(f"Expected one method named {class_name}.{method_name}")
    return methods[0]


def replace_body(source, task, generated):
    original = locate_method(source, task["class"], task["method"])
    if not isinstance(original.body[-1], ast.Pass):
        raise ValueError(f"{task['class']}.{task['method']} is no longer a placeholder")
    generated = generated.strip()
    if generated.startswith("```"):
        generated = generated.split("\n", 1)[1].rsplit("```", 1)[0]
    generated = textwrap.dedent(generated).strip() + "\n"
    tree = ast.parse(generated)
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        raise ValueError("Model must return one Python method definition")
    method = tree.body[0]
    if method.name != original.name or ast.dump(method.args) != ast.dump(original.args):
        raise ValueError("Generated method name or parameters do not match")
    if isinstance(method.body[-1], ast.Pass):
        raise ValueError("Generated method is still a placeholder")
    generated_lines = generated.splitlines(keepends=True)
    body = textwrap.dedent("".join(generated_lines[method.body[0].lineno - 1:method.end_lineno]))
    original_lines = source.splitlines(keepends=True)
    indent = " " * original.body[0].col_offset
    updated = "".join(original_lines[:original.body[0].lineno - 1]) + textwrap.indent(body, indent) + "".join(original_lines[original.end_lineno:])
    ast.parse(updated)
    return updated


def solve_task(task, index, find_chunks, client, model):
    target = (REPOSITORY / task["file"]).resolve()
    if not target.is_relative_to(REPOSITORY.resolve()):
        raise ValueError("Task file is outside the repository")
    source = target.read_text(encoding="utf-8")
    description = f"{task['class']}.{task['method']}: {task['docstring']}"
    matches = find_chunks(index, description, 5)
    context = "\n\n".join(f"{chunk['path']}:{chunk['start_line']}-{chunk['end_line']}\n{chunk['text']}" for chunk, score in matches)
    prompt = f"Implement the missing method {description}. Return only the complete method definition, without markdown. Keep its existing parameter names and defaults. Do not add imports.\n\nTarget file:\n{source}\n\nFive retrieved repository chunks:\n{context}"
    response = client.responses.create(model=model, input=prompt)
    if not response.output_text.strip():
        raise ValueError("Model returned no source code")
    updated = replace_body(source, task, response.output_text)
    target.write_text(updated, encoding="utf-8")
    print(f"Implemented {task['class']}.{task['method']} in {task['file']}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=MODELS, default="gpt-5-mini")
    args = parser.parse_args()
    load_key()
    client = OpenAI()
    index = joblib.load(INDEX)
    tasks = json.loads(TASKS.read_text(encoding="utf-8-sig"))
    find_chunks = load_matcher()
    for task in tasks:
        solve_task(task, index, find_chunks, client, args.model)


if __name__ == "__main__":
    main()
