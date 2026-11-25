"""Connect to the local server using MCP stdio and call its tool once."""
import json
from pathlib import Path
import subprocess
import sys


def main():
    server = Path(__file__).with_name("server.py")
    with subprocess.Popen([sys.executable, str(server)], stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE, text=True, encoding="utf-8") as process:
        def send(message):
            process.stdin.write(json.dumps(message) + "\n")
            process.stdin.flush()

        def request(number, method, params):
            send({"jsonrpc": "2.0", "id": number, "method": method, "params": params})
            response = json.loads(process.stdout.readline())
            if "error" in response:
                raise RuntimeError(response["error"])
            return response["result"]

        init = request(1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                         "clientInfo": {"name": "coursework-demo", "version": "1.0.0"}})
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        tools = request(2, "tools/list", {})
        result = request(3, "tools/call", {"name": "word_count", "arguments": {"text": "Codex can count these words"}})
        assert tools["tools"][0]["name"] == "word_count"
        assert result["content"][0]["text"] == "5"
        print("Protocol:", init["protocolVersion"])
        print("Tool:", tools["tools"][0]["name"])
        print("Input: Codex can count these words")
        print("Result:", result["content"][0]["text"])
        process.stdin.close()


if __name__ == "__main__":
    main()
