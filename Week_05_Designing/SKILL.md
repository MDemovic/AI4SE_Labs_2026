---
name: architecture-adr
description: Guide an interactive software architecture discussion from requirements, compare at least three viable structures, explain implementation and maintenance trade-offs, and create and revise an Architecture Decision Record (ADR). Use when choosing an architecture, reviewing an ADR, clarifying module or deployment boundaries, or repeating an architecture exercise using a recorded workflow.
---

# Architecture discussion and ADR

## Inputs and records

Read the complete supplied requirements before proposing a design. Record their source, actors, capabilities, integrations, constraints, and quality attributes. Separate confirmed requirements, planning assumptions, and unanswered product questions. Ask about missing information that could change the decision; keep useful analysis conditional when answers are unavailable.

Start a persistent discussion document at the beginning. After each substantive turn, record the user's questions or feedback, the explanation given, decisions made, and remaining questions. Label paraphrases as edited notes. Preserve actual acceptance and review history; never fabricate dialogue or turn an assistant recommendation into user agreement. Keep earlier analysis distinguishable from later revisions.

Use project-relative links between requirements, discussion notes, and ADRs. Choose output paths appropriate to the codebase and preserve existing work.

## 1. Explain and compare alternatives

Propose at least three materially different, plausible structures. Choose candidates from the requirements rather than always prescribing the same three. If comparing an application architecture with a hosting model, explain their overlap: a modular application can run on managed hosting, and background processes do not automatically constitute microservices.

For each option:

- Explain components, responsibilities, owned data, communication, and deployment in plain language.
- Walk through a representative request and one failure or concurrency scenario.
- Describe concrete implementation pain, including transactions, authorization, external dependencies, retries, and operations where relevant.
- Explain advantages and disadvantages for this system, including long-term maintenance.
- State which assumptions make the option attractive or unsuitable.

Use consistent comparison criteria: delivery effort, maintainability, operations, consistency, fault isolation, scaling, deployment independence, and provider dependency. Avoid unsupported numerical scores or claims that a hosting approach is automatically cheaper.

Invite the user to challenge the trade-offs. Answer their actual questions before moving to the decision. Do not assume that fewer components eliminate maintenance or that growth inevitably requires microservices.

## 2. Reach and record a decision

Give a provisional recommendation grounded in known requirements. Identify major costs and evidence that would change it. Distinguish code structure from hosting responsibility: managed infrastructure still leaves application authorization, configuration, migrations, monitoring, and recovery work.

Record the user's explicit choice when given. Keep the status proposed until accepted; distinguish acceptance of the architecture direction from approval of every ADR detail. Never hardcode a preferred architecture or a prior project's conclusion into this workflow.

## 3. Make boundaries and deployment concrete

For the selected design, specify enforceable boundaries rather than relying on folders or “discipline” alone:

- Assign domain behavior and persistence ownership to modules or services.
- Define public interfaces and prohibit access to another component's internal classes, repositories, and tables unless an explicitly reviewed exception exists.
- State allowed dependencies and how cycles or forbidden imports will be detected.
- Explain coordination of cross-boundary workflows and transactions. Preserve each owner's rules; do not prescribe a shared transaction across independently owned service databases.
- Define migration ownership and review of shared constraints or cascades.
- Describe planned architecture checks, integration checks, and review rules without claiming they already exist.

Describe the runtime separately from the code structure:

- Identify web/API processes, background workers or scheduled jobs, databases, and external systems.
- State which components share source code, release artifacts, versions, deployment coordination, and storage.
- Explain whether communication is in-process, through APIs, or through messages.
- Distinguish separate resource allocation from independent release ownership.
- Explain shared failure boundaries and rollout/migration coordination.

Do not mandate a queue, cache, or service solely because a background task exists. Tie mechanisms to actual scheduling, durability, throughput, and recovery needs.

## 4. Write and revise the ADR

Include these sections, combining short sections only when clarity is preserved:

1. Title, identifier, date, decision status, and source links.
2. Context, constraints, assumptions, and decision drivers.
3. Architecture decisions made now and their rationale.
4. Responsibilities, requirement coverage, and boundary enforcement.
5. Deployment structure and a diagram consistent with the prose.
6. Alternatives, benefits, costs, and reasons for selection/rejection.
7. Architecture-level correctness and failure-handling requirements.
8. Implementation details deferred, including when they must be resolved.
9. Missing product or operational requirements requiring stakeholder clarification.
10. Consequences, risks, mitigations, and revisit conditions.
11. Actual review feedback and revision history.

Keep three categories explicit:

- **Decide now:** boundaries, ownership, communication, deployment/release model, persistence approach, and essential correctness guarantees.
- **Finalize later:** provider, framework, libraries, detailed schema, locking strategy, queue necessity, retry parameters, and tooling, unless a confirmed constraint makes one architecturally decisive.
- **Clarify with stakeholders:** ambiguous features, privacy/retention policy, scale, availability, budget, and integration responsibilities. Do not treat missing requirements as developer preferences.

Deferring a mechanism must not defer security or correctness. State when the detail must be decided and which guarantees it must preserve.

Invite ADR review. Apply the user's concrete feedback and record the changes. Do not invent multiple review rounds merely to satisfy an assignment.

## 5. Check the result

Review the document for:

- Coverage of every major requirement, with no invented features treated as confirmed.
- Consistency between module ownership, workflow explanations, diagram, and deployment terminology.
- Explicit authorization, data ownership, atomicity, duplicates/retries, and external failures where relevant.
- Concrete boundary enforcement and clear operational responsibilities.
- Separation of accepted decisions, assumptions, deferred mechanisms, and unresolved requirements.
- User acceptance reflected accurately in the status and history.

Correct document inconsistencies before handing it back. Report proposed implementation checks as plans, not completed tests.

## 6. Support a fresh-session comparison

When asked to evaluate the skill, start the repeat exercise in a genuinely new session with only this skill, the source requirements, and comparable task instructions. Keep the first run's decisions, ADR, and conversation out of the repeat session until its outputs are complete. Preserve separate recordings and ADRs.

Compare requirement coverage, breadth of alternatives, explanation quality, missing assumptions, boundary/deployment clarity, and revision effort. Claim time savings only with recorded measurements and acknowledge differences in user input, model, and setup. Label a same-context replay as such; do not present it as an independent experiment.
