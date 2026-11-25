"""Minimal MCP stdio server exposing one coursework tool; Python 3 only."""
import json
import sys


def handle(message):
    method = message.get("method")
    params = message.get("params") or {}
    if method == "initialize":
        return {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}},
                "serverInfo": {"name": "coursework-tools", "version": "1.0.0"}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{"name": "word_count", "description": "Count whitespace-separated words in text.",
                           "inputSchema": {"type": "object", "properties": {"text": {"type": "string"}},
                                           "required": ["text"], "additionalProperties": False}}]}
    if method == "tools/call":
        args = params.get("arguments") or {}
        if params.get("name") != "word_count" or not isinstance(args.get("text"), str):
            return {"content": [{"type": "text", "text": "Expected word_count with a text string."}], "isError": True}
        return {"content": [{"type": "text", "text": str(len(args["text"].split()))}]}
    raise ValueError("Method not found")


def main():
    for line in sys.stdin:
        try:
            message = json.loads(line)
            if "id" not in message:
                continue
            try:
                response = {"jsonrpc": "2.0", "id": message["id"], "result": handle(message)}
            except ValueError as exc:
                response = {"jsonrpc": "2.0", "id": message["id"], "error": {"code": -32601, "message": str(exc)}}
            print(json.dumps(response), flush=True)
        except (json.JSONDecodeError, TypeError):
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}), flush=True)


if __name__ == "__main__":
    main()
