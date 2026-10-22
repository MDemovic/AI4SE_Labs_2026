# Design Report: Agentic Software Requirements Refinement

The submitted implementation is `requirements_network.py`. Its output is `requirements.md`.

## 2. Network design

The graph has six nodes. Nodes share a state containing source documents, candidate requirements, the refined requirements, candidate decisions, rejected items, open questions, review findings and a revision counter.

| Node | Type and model | Responsibility |
|---|---|---|
| `load` | Deterministic Python | Read supported files recursively, extract email text and assign source IDs. |
| `extract` | LLM: `gpt-4o-mini` | Identify candidate requirements with source evidence, uncertainty, explicit priority and a classification of requested behavior, background or question. |
| `consolidate` | LLM: `gpt-5-mini`, with Python validation | Group related candidates, account for each candidate and write requirement paragraphs. |
| `review` | LLM: `gpt-4.1-nano` | Check the whole draft for conflicts and duplicates, then compare it with original sources in batches of two documents. |
| `revise` | LLM: `gpt-5-mini`, with Python selection logic | Repair groups identified by review while preserving untouched requirements. |
| `render` | Deterministic Python | Assign final requirement IDs, check references and write the Markdown document. |

Execution begins with `load → extract → consolidate → review`. A review with findings routes to `revise`, which returns to `review`. A passed review or the limit of two revision rounds routes to `render`. If repeated unusable JSON makes a review incomplete, the draft is rendered with an explicit console warning instead of being treated as approved.

This provides at least three LLM-invoking nodes, three distinct models, deterministic processing and a feedback loop, satisfying ANS1–ANS5 at the implementation level.

## 3. Main design choices

### Extract first, then group

Extraction operates on one document at a time. Python assigns candidate IDs and source references rather than asking the model to invent them. Candidates retain an evidence quote, making later review possible.

The consolidation agent groups the complete candidate inventory before writing paragraphs. Related controls, fields and formats may be grouped into one capability.

Every candidate must have one recorded destination: a requirement group, blacklist entry or unresolved question. Deterministic validation detects missing, repeated and unknown IDs. Assignment mistakes are repaired in batches of ten. If the model repeatedly fails to assign a candidate, the script records a manual-review question rather than silently dropping it.

### Separate current behavior from desired behavior

The extraction prompt distinguishes existing-system descriptions from requested features. Candidates classified as background are removed from active groups and recorded in the blacklist. For example, an existing lack of hourly scheduling should not become a prohibition on adding hourly scheduling.

This approach prevents some false conflicts, but classification is still model-generated. A real constraint can be misclassified as background. The final run demonstrates this limitation, more below.

### Priorities and traceability

Explicit High, Medium and Low labels map to Must, Should and Could. Python sets the overall priority to the highest explicit label among the requested candidates in a group. The writing prompt asks the model to preserve different priorities for individual subfeatures. When there is no explicit label, the model estimates priority and should explain that inference.

Source IDs are derived from supporting candidates. The output includes a source-document index mapping IDs to filenames. Candidate IDs remain internal; reader-facing candidate references are converted to source IDs.

### Review and targeted revision

The reviewer is instructed to report concrete defects with requirement IDs, candidate IDs, source IDs and evidence. Sharing a general topic, such as reporting, should not be enough to justify merging two requirements.

Revision selects the implicated candidates and expands that selection to complete existing groups and decisions. The consolidation logic then rebuilds only that subset. Untouched requirement objects are preserved. A wholly missed candidate may be added when a review supplies an exact quote that occurs in the identified source document.

Two revision rounds bound the feedback loop and API cost. This limit does not guarantee that the final draft is correct.

## 4. Reliability and output format

The API calls use JSON mode, followed by parsing and validation. Reviewer responses receive additional checks for the expected issue fields. Unusable responses are retried up to three times. API requests allow 600 seconds and one transport retry.

Successfully parsed responses are cached using a hash of the model name and exact prompt. Repeating an unchanged request can reuse the saved result. Changed prompts require new calls. The cache is not a full LangGraph checkpoint: a restarted run traverses the graph again, reusing matching responses along the way.

The generated document contains only:

1. Priority scale.
2. Requirements with IDs, descriptions, priorities and sources.
3. Blacklisted requirements with reasons.
4. Open questions.
5. Source-document index.

Candidate accounting and remaining review findings are printed to the console. The large candidate ledger is not included in the deliverable. Removing that ledger does not remove the internal candidate checks.

## 5. How the output specifications are addressed

| Specification | Mechanism | Limitation |
|---|---|---|
| OS1: Single structured document | Deterministic Markdown renderer. | None observed in the final file structure. |
| OS2: Unique requirement IDs | Sequential `REQ-001` identifiers assigned by Python. | IDs may change between separate runs. |
| OS3: No semantic duplicates | Global grouping and duplicate review. | Some overlap remains. |
| OS4: Source tracing | Candidate-derived document IDs and filename index. | Source attribution does not itself prove every statement is supported. |
| OS5: Names and paragraph explanations | Writer prompt and renderer. | Some names and paragraphs are too long or cover several capabilities. |
| OS6: Explained priorities | Documented scale, explicit-label mapping and priority basis. | Inferred priorities and paragraph wording can still be inconsistent. |
| OS7: Consistency | Conflict review, background classification and revision. | Remaining contradictions were observed. |
| OS8: Completeness | Per-document extraction, candidate accounting and original-source review. | Accounting for candidates does not prove that every source requirement was extracted or correctly retained. |
| OS9: Blacklist with reasons | Rejected/background candidates rendered with explanations and sources. | Some entries appear to have been rejected too aggressively. |

## 6. Validation and observed run

The script was ran against the supplied corpus through the API. The submitted terminal excerpt ends with a successful file write and no traceback. It explicitly reports that review did not pass completely.

| Observed item | Result |
|---|---:|
| Documents in the source index | 20 |
| Final numbered requirements | 24 |
| Candidates accounted for in the console audit | 318 / 318 |
| Blacklist bullet entries | 51 |
| Open-question bullet entries | 24 |

The candidate total is the final accounted inventory reported by the run; it is not independently verified against every sentence in the original corpus. This evaluation used the generated document and supplied terminal excerpt, rather than a new exhaustive source-by-source audit.

## 7. Remaining limitations

The final output demonstrates the network, but it is not a fully validated specification:

- **Privacy conflict:** REQ-016 limits any reporting output to anonymized data without personally identifiable information, while REQ-009 requests mailing addresses. Privacy restrictions need a defined scope instead of a blanket rule.
- **Project task included as a software requirement:** REQ-020 assigns responsibilities to a working group. It should be distinguished from required software behavior.
- **Overlapping and broad groups:** REQ-010 combines platforms, accessibility, permissions and environments. Environment/migration behavior also appears in REQ-016, and role behavior appears in REQ-011 and REQ-022.
- **Question/requirement inconsistency:** The open questions ask whether null demographic values should be included even though REQ-008 already specifies null handling. Other questions similarly reopen decisions made in the requirements.
- **Over-aggressive background classification:** Blacklist entries include privacy, retention and vendor-integration statements that may express genuine constraints. Their exclusion needs source-based human assessment, even where related behavior survives elsewhere.
- **Reviewer false positives:** The terminal review says that transit-to/transit-from merging is missing, although REQ-005 explicitly includes it. Some findings describe hypothetical conflicts or even affirm that a requirement is correct. Such feedback can cause unnecessary revisions.
- **Priority inconsistency:** Explicit group labels are controlled in Python, but paragraph wording and inferred priorities remain model-generated. They do not always preserve the intended distinctions.

## 8. Running the submission

Install dependencies with Python 3.11 or a compatible Python environment:

```powershell
py -m pip install langgraph langchain-openai
```

Set the API key in the PowerShell session, then run from the folder containing the script:

```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
py .\requirements_network.py --input-dir ".\data\corpus" --output ".\requirements.md"
```
