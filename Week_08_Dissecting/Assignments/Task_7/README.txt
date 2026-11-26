Task 7 - Local MCP server

server.py is a minimal stdio MCP server written with the Python standard library. It exposes one tool, word_count, which counts whitespace-separated words. No package installation is needed. demo.py starts the server, initializes the MCP connection, lists the tool and calls it once.

From the repository root, run:
python Week_08_Dissecting/Assignments/Task_7/demo.py

The server is registered in the repository's .codex/config.toml. A copy of that configuration is in codex-mcp-config.toml. The absolute path must be adjusted if the repository is moved to another computer.

In a new Codex session started from the repository, ask it to use the coursework word_count tool and approve the tool call if prompted. Result_Task7.txt records a successful native Codex tool call as well as the separate demo.py test.
