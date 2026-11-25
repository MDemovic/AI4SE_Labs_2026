Task 7 - Local MCP server

server.py is a minimal stdio MCP server written with the Python standard library. It exposes one tool, word_count, which counts whitespace-separated words. No package installation is needed. demo.py starts the server, initializes the MCP connection, lists the tool and calls it once.

From the repository root, run:
python Week_08_Dissecting/Assignments/Task_7/demo.py

To make it available to Codex CLI, register it using the full path to server.py:
codex mcp add coursework -- python C:\AI-Soft\AI4SE_Labs_2026\Week_08_Dissecting\Assignments\Task_7\server.py

Restart Codex and ask it to use the coursework word_count tool. The demonstration in demo.py calls the tool through MCP; it is a separate client rather than a recorded Codex MCP tool call.
