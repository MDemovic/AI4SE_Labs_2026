# Repository Guidelines

## Project Structure & Module Organization

Course work is grouped by topic in `Week_03_Prompting/`, `Week_04_Requirements/`, `Week_05_Designing/`, `Week_06_Implementation/`, and `Week_08_Dissecting/`. Task folders contain their instructions, reports, scripts, and supporting data or images. `Assessments/` holds assessment documents. The Week 6 Task 1 playground contains Python modules in `AI4SE_Playground/playground/playground/` and tests in the adjacent `tests/` directory. Keep new work with its corresponding week and task.

## Build, Test, and Development Commands

There is no repository-wide build. Run task-specific scripts from the repository root unless their instructions say otherwise:

- `python Week_03_Prompting/Assignments/Task_4/analyze_results.py` reproduces the Week 3 analysis; it requires `numpy` and `matplotlib` and recalculates Task 3 metrics.
- `python -m pip install -r Week_06_Implementation/Assignments/Task_3/requirements.txt` installs the embedding task's dependencies. Task 5 has its own `requirements.txt`.
- From `Week_06_Implementation/Assignments/Task_1/AI4SE_Playground/playground/`, run `python -m unittest discover -s tests` to discover the playground tests.

Check each task's Markdown instructions and script `--help` for inputs and outputs before running it; scripts may regenerate tracked results.

## Coding Style & Naming

Follow the surrounding code: use four spaces for Python indentation, `snake_case` for modules and functions, and `PascalCase` for classes. Name assignment files consistently with existing examples such as `Task_3.md` and `Task_3_report.txt`. Use descriptive Markdown headings and keep data and figures near the report that uses them. No repository-wide formatter or linter is configured.

## Testing Guidelines

The playground uses Python's standard `unittest` framework. Add focused tests in `tests/test_*.py` for behavior changes and run the discovery command above. For analysis scripts, check outputs against the relevant input data and document reproduction steps. No coverage threshold is specified.

## Commits & Pull Requests

Recent history uses short, descriptive subjects such as `Finish task 5` and `Week 03 assessment`. Follow that concise style and identify the task affected. In pull requests, describe the assignment and changes, list checks performed, and link any relevant issue; include images when visual output changes.

## Configuration & Agent Guidance

Keep API keys out of commits; Week 6 Task 5 reads `OPENAI_API_KEY` from the environment or a local `.env` file. When helping with assignments, briefly explain significant choices so the student can understand and review the work.