# Architecture discussion — working record

- **Started:** 2026-10-29
- **Status:** **Option B (modular monolith) accepted by the user as OneSport’s architecture direction on 2026-10-29.** Detailed implementation choices and full ADR text remain subject to review. Release 1 supports ticket browsing/saving without purchases; no established backend preference.
- **Workflow:** [Architecture discussion and ADR skill](../SKILL.md)
- **Requirements source:** [OneSport requirements](../OneSport.txt) (system description and US01–US24)
- **ADR:** [ADR-0001 — OneSport application architecture](ADR-0001-onesport-architecture.md) — **Accepted (architecture direction only), revision 0.4; detailed design pending review.**

## Session 1 — 2026-10-29

### User input (verbatim)
> run the skill

### Edited notes — assistant response
- The uploaded skill directs an interactive architecture assessment, comparison of at least three materially different structures, and creation/revision of a proposed ADR.
- No project description, requirements document, or codebase was provided with the request. Architectural choices are therefore deliberately not invented.
- Requested the user's system requirements or a short project description to begin the comparison.

### Confirmed requirements
- None supplied yet.

### Planning assumptions
- None about technology, scale, data, integrations, or operations.

### Outstanding questions
- What system is being designed or reviewed? Please share requirements, a relevant existing ADR, or a project description, including main users, capabilities, constraints, and integrations if known.

### Decisions and review history
- No decisions made.
- No user acceptance or review feedback received.


## Session 2 — 2026-10-29 — OneSport architecture comparison

### User input (verbatim)
> These are the OneSport requirements. Use the skill to guide me through comparing three architectures. Keep notes throughout our discussion, then help me choose an architecture and create an ADR for review. Save the notes and ADR as separate files for this run.

### Source and interpretation (edited notes — assistant analysis)
- Read the complete [OneSport.txt](../OneSport.txt): system description and 24 user stories; no implementation, budget, load or operating constraints supplied.
- Sole **confirmed actor**: User. No confirmed administrators, sellers, providers, payment processors or support operators.
- **Accounts (US01–US06):** registration, login, logout, profile settings, account deletion, change email/password.
- **News (US07–US08):** recent news and selecting Italian news from country options. **Ticket discovery (US11–US12):** upcoming available tickets and selecting Italian tickets from country options.
- **Saved content (US09–US10, US13–US15, US20–US21):** save/remove/view favorite news and saved tickets, clear news and ticket saved items. US15 calls them the "favourite list"; whether one combined list or two collections is unspecified.
- **Social (US16–US19, US22–US24):** send/view/accept/decline friend requests, remove friends, find users by email, view friends and their details.
- **Product narrative:** calls OneSport a destination for *purchasing tickets*, but none of US01–US24 requires actual checkout, payment, reservations, ticket issuing or refund processing. Treat purchase functionality as an unresolved scope question, not a confirmed feature.
- **Confirmed quality intent:** "up-to-date" sports information, convenience, engagement. No measurable freshness, performance, uptime, geographic availability or privacy policy is specified.
- **Confirmed integrations:** none explicitly. A news feed, ticket inventory/affiliate feed, external identity provider, and payment partner are possible **planning assumptions only**, not requirements.
- **Constraints not supplied:** existing codebase/framework, team size, cloud/provider, budget, intended users/traffic, data retention rules, security/compliance target, SLAs, rollout schedule, and integration/licensing terms.

### Planning assumptions for conditional design (not user decisions)
- MVP includes the 24 listed stories, not on-platform purchase/checkout unless clarified.
- A web interface and a server/trusted logic path are plausible, but client type and hosting are unconfirmed.
- User accounts, saved items and friendships need reliable persistent storage, access control, duplicate prevention and account-deletion semantics.
- News and ticket information might be provider-fed; no specific provider, update strategy, API or legal rights assumed.
- Relational storage is a *candidate* based on account relationships and atomic friend-request transitions; it is not mandated by the requirements.

### Options compared (edited notes — assistant explanation)

#### A. Managed backend / serverless (BaaS-first)
- **Code/runtime:** browser frontend + managed identity and database with authorization policies; trusted serverless functions for friend workflow, account-deletion coordination, provider credentials and catalog ingestion; scheduled functions only if freshness needs them. Several functions may deploy independently. Managed provider operates data-plane infrastructure, not the application's authorization rules or recovery policy.
- **Data ownership/communication:** identity in managed auth, account profile/social/saved/catalog records in managed database with explicit access policies; client talks to managed APIs for safe reads and trusted functions for sensitive writes. Cross-table DB transactions if provider supports them; identity-provider operations remain external.
- **Representative request:** accept friendship: UI sends authenticated request to function; function confirms recipient, checks request state, commits acceptance and symmetric friendship relation in a database transaction, returns result. No direct client permission to forge friendships.
- **Failure/concurrency:** double acceptance or crossing invitations must be idempotent via normalized pair uniqueness and transactional state changes; function timeouts can produce uncertain outcomes and require safe read/retry. Provider-wide outage blocks dependent features.
- **Concrete implementation pain:** expressing email-based directory privacy and reciprocal friend rules in row-level policies/functions; credential management; local/emulator tests and schema migrations; external catalog rate limits; deleting a managed identity and associated records cannot necessarily be one atomic transaction.
- **Advantages:** smaller custom server surface, managed identity/hosting operations, potentially quick MVP under a team's provider familiarity.
- **Costs/maintenance:** policy code dispersed across functions and database rules; vendor-specific security and query model; quotas and cost shape must be validated, not assumed cheaper; function/version coordination and data export strategy. Attractive if the team prioritizes speed and accepts a provider ecosystem; weaker if cross-domain rules grow or portability is essential.

#### B. Modular monolith + relational database (provisional recommendation)
- **Code/runtime:** one backend deployable with strict Accounts, NewsCatalog, TicketCatalog, SavedItems, Connections domains and an HTTP/API composition layer; one relational database; browser frontend; optional same-version periodic ingester/worker if data freshness requires it. Managed hosting can run the monolith; optional workers do **not** make it microservices.
- **Data ownership/communication:** each module owns its domain rules, repositories/tables and migrations; module-to-module calls use documented interfaces in-process. Backend coordinates database transactions while preserving module invariants. External content/provider adapters, if any, stay behind catalog interfaces.
- **Representative request:** accept friendship: API authenticates recipient, calls Connections.accept(requestId, actorId); Connections checks authorization and pending state, atomically transitions request and creates a unique unordered friendship relation, returning success or a safe, distinguishable outcome for an invalid request.
- **Failure/concurrency:** two concurrent accepts or reciprocal invitations resolve under unique keys/transactional checks; retries cannot create duplicate friendships. If a catalog provider times out, catalog endpoints return a defined stale/unavailable state, rather than silently presenting unverified inventory as available (freshness policy TBD).
- **Concrete implementation pain:** enforce boundaries rather than merely separate folders; maintain migrations and cross-module API contracts; design full account removal across domain-owned tables and possible external identity provider; operate API/DB backups, monitoring, deployments and security.
- **Advantages:** strong local consistency for friendships/saved lists; fewer network hops; one coordinated backend release; future extraction possible if real scaling/ownership need emerges; domain-specific code organization aids maintainability.
- **Costs/maintenance:** backend deployment is a shared fault/release boundary; whole backend typically scales together; modularity needs architecture tests and review discipline. Attractive for tightly related user flows without evidence of independent service demands; weaker under strict separate team ownership or radically different subsystem scaling/security requirements.

#### C. Independent domain microservices
- **Code/runtime:** independently deployable Accounts, Content (news/ticket catalog), SavedItems and Social services behind a gateway/BFF; each service owns its data store and migration lifecycle. Calls via HTTP/RPC; events or messages only where needed for durable asynchronous workflows. Catalog sync as a task within its owning service if needed.
- **Data ownership/communication:** no cross-service reads of another service's tables or shared transactions. SavedItems holds references to Content IDs, Social to Accounts IDs. Cross-service data validation, deletion and change propagation require explicit protocols and idempotency.
- **Representative request:** save a ticket: gateway authenticates user; SavedItems optionally queries Content for canonical ticket offer ID and stores an idempotent preference. Saving does **not** reserve a ticket; stale ticket availability is handled independently of saving. Return a clear degraded response if validation is unavailable.
- **Failure/concurrency:** a ticket provider or Content service can fail while SavedItems remains up; the workflow must choose between rejecting the save and storing an unvalidated reference, then reconcile. Account removal fans out to multiple owners without a global transaction; retries and partial completion need explicit tracking. Social service itself maintains atomic friend invariants in its own store.
- **Concrete implementation pain:** contract/version evolution, service-to-service auth, distributed tracing, API timeouts, retries/deduplication, drift in references, data deletion, multiple delivery pipelines and operational on-call.
- **Advantages:** independently deployable/scaleable domains and fault containment when dependency paths permit; supports genuinely independent teams.
- **Costs/maintenance:** substantially more operational coordination and eventual consistency, especially for user deletion; services can still fail together through dependencies. Attractive if teams/release cadences or proven scale/security isolation justify this complexity, not simply because OneSport has five features.

### Side-by-side assessment (qualitative; no numerical scores)

| Criterion | A: Managed backend / serverless | B: Modular monolith | C: Microservices |
|---|---|---|---|
| Initial delivery | Often fastest with platform expertise; policy complexity can offset | Moderate: build backend, but straightforward local domain flows | Heaviest due to service contracts and platform setup |
| Maintainability | Vendor rules/functions can become fragmented | Explicit in-process modules and shared repo; boundary checks required | Clear ownership possible; distributed contracts and drift grow |
| Operations | Provider handles more infrastructure; team still owns app security/migrations/monitoring | One API release, database and optional same-release worker | Several deployments, observability, recovery paths |
| Consistency | Strong within supported database transactions; identity external | Strong local transactions in one DB | Local to services; cross-service workflows eventual |
| Fault isolation | Managed provider outages can hit several capabilities | Shared backend is common failure boundary | Partial isolation, not if synchronous dependencies cascade |
| Scaling | Managed service/function scaling subject to quotas/provider behavior | Horizontally scale backend; DB or individual module can become bottleneck | Independently allocate capacity to hot domains |
| Deployment independence | Functions individually deployable, database policies coordinated | One backend release (frontend may deploy separately) | Per-service releases, with versioned contracts |
| Provider dependence | Typically high on managed identity/data primitives | Hosting/provider swappable with integration work | Depends on each service/platform; infrastructure burden high |

### Provisional direction and reasons (edited notes — not user approval)
- **Recommend B, modular monolith**, tentatively: shared account/social/saved-item invariants fit a single transaction boundary, and the requirements do not establish independently scaling teams or domains. Organize by business responsibilities, not by controller/database-layer folders.
- **Not yet a chosen/accepted architecture**. A may win if time-to-MVP, low infrastructure staffing and managed provider expertise dominate. C may win if multiple independent teams, hard isolation mandates or evidenced asymmetric scaling/release needs emerge.
- Managed infrastructure is compatible with B; the managed-vs-self-hosted choice must be evaluated separately from modular application boundaries.
- Ticket purchases are excluded from the provisional scope pending clarification; if payment/reservation is required, the architecture needs explicit order/payment boundaries, non-oversell requirements and external transaction recovery.

### Stakeholder questions that could change the decision
1. Is OneSport's first release **ticket discovery/saving only**, a redirect to an external seller, or complete in-app purchasing and issuance?
2. Where do news and tickets originate (editor-curated/internal, third-party data APIs, affiliates, actual sellers), and what data/license/freshness guarantees apply?
3. Team size, experience, target launch window, and platform or technology constraints?
4. Peak usage, acceptable content staleness, regional reach, uptime goals, recovery objectives and operating budget?
5. What user information may exact-email search reveal? How are accounts, friendships and saved data handled for privacy, deletion, retention and backups?
6. Should "clear all" clear both categories together, and should saved tickets persist after the underlying listing expires?

### Decisions, user feedback and review history
- User instructed comparison of three architectures, continuous notes and an ADR for review.
- No acceptance/rejection of a candidate has been provided; no actual ADR review feedback yet.
- Assistant has proposed B conditionally and documented open questions; this is **not** a recorded user decision.
- ADR draft created as [ADR-0001](ADR-0001-onesport-architecture.md). Next step: user compares trade-offs, challenges them, clarifies ticket purchasing and optionally selects a direction; revise both files and record real feedback.


## Session 3 — 2026-10-29 — Ticket scope confirmation and architecture evaluation

### User input (verbatim)
> The first OneSport release only supports browsing and saving tickets, with no purchase flow. Continue the architecture discussion using the skill, update the discussion notes and proposed ADR, and help me evaluate the recommendation.

### Confirmed product-scope decision (not an architecture acceptance)
- **Release 1 ticket capability:** browse upcoming ticket listings, filter by country, save/list/remove/clear saved ticket references. **No purchase flow**. This user clarification resolves the release-1 ticket-purchase ambiguity left by the broader product narrative in [OneSport.txt](../OneSport.txt).
- **Explicitly outside release 1:** on-site checkout, payment initiation/processing, orders, inventory holds/reservations, ticket issuance, refunds/cancellations and an external checkout/redirect flow. These are not needed for the supplied first-release features. Whether purchasing ever belongs on the roadmap remains undecided.
- **Do not conflate** a user's saved ticket/listing with a purchased ticket, stock reservation, or guaranteed current availability. US13's phrase “purchase them later” establishes why someone saves tickets, **not** a current purchase feature.
- All US01–US24 remain the functional basis; no new features were invented by this clarification.

### Edited notes — updated evaluation of the three alternatives
- **A — Managed backend/serverless** becomes more appealing for a narrow first release because ticket workflows only need catalog reads and simple preference writes, not payment/order orchestration. However friend-request acceptance still requires server-authoritative authorization, uniqueness and atomic transitions; managed database policies/functions, account deletion and provider data sync require engineering and ongoing maintenance. Prefer A *if* existing platform expertise, delivery urgency and willingness to accept vendor coupling clearly dominate.
- **B — Modular monolith** remains the **provisional recommendation**, not user-selected. One deployable backend with domain-owned Accounts, NewsCatalog, TicketCatalog, SavedItems and Connections modules and one relational database can give straightforward local friend-request transitions, durable saved references and controlled account deletion. With no sales lifecycle, there is no reason to introduce an Orders/Payments domain or purchase-specific distributed coordination. Hosting the backend and DB on managed infrastructure is compatible with B.
- **C — Independently deployed microservices** is even harder to justify solely from current stories: no order/payment service, no user evidence of separate teams, independent release requirements or scale/fault-isolation targets. More contracts, distributed account-deletion orchestration and service operations buy little for the known scope. Revisit if explicit autonomy, measured bottlenecks, or mandated isolation becomes real.
- This is a **qualitative judgment**; there are no verified team, provider, price, load or service-level inputs to justify an objective cost or speed ranking.

### Implementation consequences of confirmed scope (edited notes)
1. `TicketCatalog` owns *informational listing metadata* and its provenance/freshness if a feed exists, **not** purchase inventory holds or payment orders.
2. `SavedItems` stores unique user-to-listing references; saving and removing are idempotent. A listing disappearing or expiring must be handled according to a stakeholder-defined saved-reference policy; do not pretend saving secures a ticket.
3. `Connections` still requires an atomic accept-friend transition and uniqueness per unordered pair; this is a stronger driver of relational transactions than ticket browsing.
4. `Accounts` still needs deletion and credential/security semantics; none vanish because purchase is deferred.
5. Content retrieval/refresh and managed auth remain optional **integration choices**, not confirmed requirements. Schedule/queue/cache/worker mechanisms should be justified only by agreed freshness and reliability targets.
6. Primary architectural shape can be selected without choosing framework, cloud or exact schema; these can be finalized later while preserving the documented guarantees.

### Remaining questions ranked by architectural impact
1. **Team/platform/delivery:** Who will build and operate OneSport, what backend or BaaS experience already exists, is there an existing codebase, and how tight is launch time? This is the leading factor that could swing B versus A.
2. **News/ticket listing source and freshness:** editorial data or third-party providers, allowed use/licensing, refresh expectations and meaning of ticket availability. This affects external adapters and whether scheduling is necessary, not necessarily the application architecture.
3. **Scale and nonfunctional constraints:** active users, peak event traffic, availability objectives, geography and operational budget. Evidence of independent scaling or release requirements could reopen C.
4. **Privacy and deletion:** allowed email directory visibility, profile fields, friend-list permissions, retention, backups and behavior on account deletion.
5. **Saved-content semantics:** confirm whether one action clears both saved content types and what happens to saved references when a listing/article is removed.

### Decisions, review and revision history
- **Accepted product clarification:** Release 1 supports ticket browsing and saving only; no purchasing flow.
- **Not accepted or chosen:** A, B or C; the user has not selected an architecture or approved ADR detail.
- **Assistant analysis:** Retained Option B as a provisional preference; Option A remains a plausible MVP choice dependent on provider/team constraints; Option C lacks current justification.
- Updated [ADR-0001](ADR-0001-onesport-architecture.md) to **draft 0.2**, recording confirmed scope, reduced ticket responsibilities, current rationale, unresolved issues and actual clarification feedback. No fabricated reviewer approval.
- **Next user decision invited:** describe team/technology/hosting constraints and challenge the comparison, then explicitly choose an architecture direction or request a revision.


## Session 4 — 2026-10-29 — No established backend preference; architecture choice guidance

### User input (verbatim)
> We have no established backend preference. Help us choose an architecture for OneSport based on its requirements, and continue updating the notes and ADR.

### Confirmed input and non-inferences
- **Confirmed:** The user/team has **no established backend preference**. No framework or BaaS platform should be treated as a preselected constraint. The prior release-1 decision remains browsing and saving tickets with **no purchase flow**.
- **Not confirmed:** That the team has no backend experience, no codebase, unlimited development time, a particular budget, a particular deployment provider, or a specific load profile. Absence of a *preference* does **not** establish absence of skills or integrations.
- **Still source-backed functional scope:** US01–US24 in [OneSport.txt](../OneSport.txt): Accounts, NewsCatalog, TicketCatalog (informational listings), SavedItems and Connections. No new story has been added.

### Edited notes — decision analysis without a preferred backend
1. **Choose architectural shape before framework/provider.** The requirements feature cohesive identity, profile and friend workflows, two catalog reads/filters, and saved references. Correctly handling authenticated writes, unique saves and concurrent friend acceptance is important; none of the supplied stories requires independently deployable services.
2. **Recommended choice for review: Option B, a modular monolith on managed infrastructure.** This is one modular backend release using an HTTP API and a relational database with domain-owned tables. Hosting the application and database through managed services is compatible with B; managed hosting does not make it Option A's direct managed-data/BaaS-first architecture.
3. **Why B beats A on currently known evidence:** Without an established platform preference, we cannot count familiarity with a BaaS as a verified speed advantage. B gathers privacy-sensitive directory lookup, social transitions and account lifecycle rules behind coherent application interfaces; it leaves more room to select providers later. **Counterargument:** If the only real team capacity is frontend-oriented, there is a near-term deadline, and a managed auth/database product suits all access rules, Option A may provide better initial delivery and less application-hosting responsibility. Neither cost nor velocity is established without team/workload evidence.
4. **Why B beats C on currently known evidence:** A single transaction scope for Connections and saved-item operations avoids additional service contracts, retry/reconciliation protocols and distributed account deletion across independently owned databases. Requirements supply no independently releasing domain teams, workload measurements, or hard domain isolation mandates. **Counterargument:** A real organizational split, verified asymmetric scaling, or strict isolation constraints might justify independently owned services later.
5. **Narrow implementation commitment:** Start with Accounts, NewsCatalog, TicketCatalog, SavedItems and Connections as separate internal modules with owned data and public interfaces. Keep one API backend deployable and one relational DB. HTTP is between UI and backend, **not between these modules**. No queue, cache or catalog worker is required merely because feeds might eventually exist. If needed, a catalog refresh process shares backend version/release ownership.
6. **Managed infrastructure decision is separate:** Consider managed database, application hosting, and possibly managed identity for operations relief. The chosen auth solution and deletion/revocation semantics need design review before coding Accounts. Framework, vendor, schema specifics and ingestion mechanism stay deferred, not assumed.
7. **Practical decision test:** Prototype two vertical slices before locking in provider/framework: (a) authenticated save/remove/list ticket reference with unique constraint and appropriate authorization; (b) request/accept friend with duplicate and concurrent acceptance tests. Exercise account deletion across owned tables and a simulated catalog-feed failure. These are **proposed checks**, not completed work. If they prove unusually complex in B or show a decisive BaaS advantage, revisit A.

### Updated head-to-head trade-offs (same criteria, no invented scores)

| Criterion | A — managed BaaS-first | **B — modular monolith (recommended)** | C — microservices |
|---|---|---|---|
| Delivery effort | Can be fast with suitable service/policy expertise; unverified for this team | Moderate, focused on one coherent backend | Service and infrastructure setup high |
| Maintainability | Policies, database logic and functions can fragment | Modular contracts and one repository; boundary tests needed | Many API contracts/versioning and coordination tasks |
| Operations | Provider runs more infrastructure; team still owns authorization, migrations and incidents | Team owns API behavior and operations; managed compute/DB can reduce infrastructure work | Many deployables, monitoring/recovery paths |
| Consistency | Supported database transactions; identity deletion may be external | One relational transaction scope, preserving domain ownership | Local only; cross-service recovery needed |
| Fault isolation | Functions may be isolated, but provider is a common dependency | Shared backend failure/release boundary | More potential isolation, but dependent calls can still fail together |
| Scaling | Provider-managed within constraints | Scale API replicas/DB first, measure bottlenecks | Independently scale service processes and stores |
| Deployment independence | Functions sometimes independently released; DB policy coordination remains | Backend modules ship together | Independent service releases with contract compatibility |
| Provider dependency | Often high to selected auth/database platform | More hosting choice, with migration work still necessary | Depends on stack; costs of distributed operations persist |

### Recommendation, challenge and acceptance gate
- **Assistant recommendation (not user agreement):** Proceed toward **Option B**, with a managed relational database and managed backend hosting if useful, while keeping framework/vendor unselected. The first release needs **no payment, orders, holds, tickets issued, message broker, or microservice split**.
- **Material evidence that would overturn it:** firm launch deadline combined with demonstrated BaaS effectiveness/team limitations; existing application constraints discovered; strict module-level isolation/regulatory demands; separate product teams requiring independent releases; workload measurements showing large domain skew.
- **Primary unresolved stakeholder issues before production:** catalog source/licensing/freshness; account-directory email visibility and profile permissions; deletion/retention incl. backups and external identity; scale/availability/budget; US15 clear-all semantics and behavior for expired saved references.
- **Architecture acceptance remains pending.** Invite user to explicitly endorse B as an *architecture direction* or challenge the trade-offs. Accepting B would not automatically approve every ADR detail or select a vendor/framework.

### Decisions and revisions recorded in this turn
- **Confirmed:** No established backend preference. Prior confirmed no-purchase release-1 scope is unchanged.
- **Not confirmed:** No architecture selection or formal ADR approval by the user yet.
- **Assistant action:** Reassessed A/B/C using the confirmed scope without claiming a skill/vendor advantage; maintained B recommendation and added explicit decision test, possible overturn conditions, and downstream review topics.
- **Artifacts:** Updated this [discussion record](discussion.md) and [ADR-0001 draft 0.3](ADR-0001-onesport-architecture.md) as separate files for the same run.


## Session 5 — 2026-10-29 — Explicit acceptance of architecture direction

### User input (verbatim)
> I accept Option B, the modular monolith, as OneSport's architecture direction. Update the discussion notes and ADR to record this acceptance, while keeping detailed implementation choices subject to review.

### Decision recorded — user acceptance (not assistant inference)
- **Accepted on 2026-10-29:** **Option B — modular monolith** is the architectural direction for OneSport. In the compared option, this means one logically modular backend application with a coordinated backend release and a relational persistence approach. Managed hosting is compatible but **not** chosen or approved as a particular implementation.
- **Acceptance boundary:** This is **direction-level acceptance**, **not** wholesale approval of ADR-0001's interfaces, all boundary specifications, detailed module APIs, deployment provider, database engine, identity mechanism, exact schemas, transactions/locking tactics, operational targets, or implementation plan. Those remain reviewable and can be revised without misrepresenting the user's choice.
- **Confirmed product scope carried forward:** first release browses and saves ticket listings; there is **no purchase, checkout or reservation flow**. The team has **no established backend preference**; do not invent framework or provider preferences.

### Edited notes — outcome, reasoning and resulting work
- The acceptance follows prior qualitative comparison of **A (managed backend/BaaS-first), B (modular monolith), C (independent microservices)** across delivery effort, maintainability, operations, consistency, fault isolation, scaling, independent deployment and provider dependence; see Sessions 2–4. No new technical evidence or requirements were supplied this turn.
- The reviewed **direction** is to keep Accounts, NewsCatalog, TicketCatalog, SavedItems and Connections as coherent module candidates, with protected in-process interfaces, module-owned data and single-release coordination. Module names/public signatures and the precise enforcement implementation are **proposed elaborations**, not separately ratified details.
- **Costs acknowledged from the comparison:** backend deployment/failure boundary is shared; domain boundaries require real enforcement; changes and migrations require coordinated release practices. These are accepted as architectural trade-offs in principle, not evidence that a specific operating plan has been approved.
- Updated [ADR-0001](ADR-0001-onesport-architecture.md) to **revision 0.4**, with status **Accepted — architecture direction only; detailed implementation pending review**. Preserved prior comparisons and chronological, historical "not accepted" notes as the record of earlier sessions.

### Open review items — not decided by this acceptance
1. Confirm catalog source, licensing, update frequency, freshness and ticket-listing availability semantics.
2. Agree on email lookup privacy, permissible user-profile disclosure, and abuse controls for directory search.
3. Define account deletion/retention behavior, external identity coordination if used, and backups.
4. Clarify saved-items clear-all semantics and expired/missing item handling.
5. Establish team/operating responsibilities, delivery deadline, scale, service objectives and budget; choose framework, deployment and database providers based on those constraints.
6. Review proposed module interfaces, boundaries, transaction/uniqueness strategy, migration ownership and architecture checks before implementation.

### Review history and next step
- **Actual user architecture acceptance:** Option B direction, explicitly stated in Session 5.
- **Not yet provided:** approval of all ADR details, implementation selections, or resolved stakeholder questions.
- **Next review:** examine [ADR-0001](ADR-0001-onesport-architecture.md) sections 3–8 and provide corrections or approval of individual design choices as information becomes available. Do not silently upgrade this limited acceptance to full ADR sign-off.
