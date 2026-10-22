# Refined Software Requirements

## Priority scale

- **Must:** Essential for the system's core needs.
- **Should:** Important, but a reasonable first release can work without it.
- **Could:** Useful but optional.
- Source priorities map High to Must, Medium to Should, and Low to Could.
- Other priorities are estimates; each requirement includes the reason.

## Requirements

### REQ-001 — Material volume and point-in-time inventory reporting

Material Volume and Point-in-Time Inventory Reporting: The system should provide the ability to report material volume for a given library at any specified point in time (via date filters), showing counts that include new acquisitions (recently added items), items on the shelf (checked in), items out in circulation (checked out), and holds; the report should support category breakdowns (for example total items in library, number of holds, adult fiction, board books and other user-configurable categories) and should be able to present historical volume changes over time (time-series/trend output) for the selected library and date(s).

**Priority:** Should  
**Priority basis:** All source candidates describe these capabilities with language such as “should” or “can” (no source assigns a higher priority), so a medium priority (Should) is inferred; no conflicting source priorities were provided.
**Sources:** DOC-001, DOC-010, DOC-015

### REQ-002 — System capacity dashboard (overview, drill-down, filtering and export)

System Capacity Dashboard: The dashboard must provide a high-level overview of capacity for all branches at once and must allow users to drill down into individual branches; it must provide sorting and filtering of the displayed data by region, type and load; it should display capacity trends (e.g., whether a branch is growing or shrinking) and should support cross-branch comparison reports; the dashboard should allow users to export the currently filtered/sorted/drilled view to CSV for directors who require spreadsheets.

**Priority:** Must  
**Priority basis:** Multiple requests in the design and conversation drafts explicitly ask for an interface showing all branches, drill-down and filtering (high-level, DOC-002 and DOC-010), so those features are treated as Must; trend display, cross-branch comparison and CSV export are called out in the conversation draft and meeting minutes and are therefore treated as Should.
**Sources:** DOC-002, DOC-010, DOC-018

### REQ-003 — Material-volume, point-in-time inventory and shelf-space comparisons (per library & system)

Material-volume and Shelf-space Comparison (per library & system): For each combination of genre and format, the system should produce comparative, point-in-time inventory and shelf-space reports that, for a selectable date (including a specified historical date), show the percentage of total circulations, the percentage of the collection, and the percentage of total shelf space; these reports must be available both per individual library and for the entire system and must include a side-by-side comparison view that displays each library's breakdown adjacent for easy comparison, with historical snapshots reflecting the inventory and shelving state as of the selected date even if items' shelving locations have changed since that date.

**Priority:** Should  
**Priority basis:** Most sources use 'should' phrasing for the requested comparisons and fields (percentages of circulations, collection, and shelf space) and per‑library/system availability; a side-by-side view was suggested as a lower-priority 'can we' request; historical point-in-time reporting was explicitly requested by users.
**Sources:** DOC-003, DOC-010, DOC-015, DOC-020

### REQ-004 — Batch item transfer and relocation utility (query, save, select, move, pull lists, auto-revert, labels, alerts, permissions, history)

The system must provide a Batch Item Transfer and Relocation utility that: Must allow staff to query candidate items for transfer and Must allow manual selection of titles from query results; Must enable batch modification of item records (including changing the location field) to move selected items to a target branch; Must present a preview of all proposed changes before they are applied and Must provide an undo function to revert a recent batch operation; Must enforce permissions so only authorized staff can initiate or apply transfers and Must record a persistent transfer history for auditing; Should allow saving and reusing queries for repeated use and Should generate pull lists to support physical retrieval workflows and Should support auto-revert operations (including scheduled checks and event/status‑based criteria to return items to their original location after a set period or specified conditions); Should send alerts when transfers are delayed or encounter issues; Could provide printable transit labels (for example, barcode labels) for items being moved.

**Priority:** Must  
**Priority basis:** Multiple provided requests explicitly ask for batch transfers, querying and saving queries, manual selection, record/location changes to move items, pull lists, preview and undo, permissions restrictions, transfer history, scheduled/event-based auto-revert, printable transit labels, and alerts; preview, undo, permissions, history, query and move functions were repeatedly emphasized so those were inferred Must, supporting features were inferred Should and labels inferred Could.
**Sources:** DOC-004, DOC-010, DOC-015

### REQ-005 — Missing, damaged and in-transit item reporting (branch & system scope; merged transit-to/from; configurable in-transit threshold)

Missing, Damaged and In-Transit Item Reporting — The system should provide a combined reporting capability, available per branch and for the entire system, that (a) produces reports of missing and damaged items by branch, (b) generates an in-transit items list showing items that have been in transit longer than a configurable threshold X days (X configurable) both per branch and for the whole system, and (c) merges transit-to and transit-from records into a single transit report to simplify use by front-line staff.

**Priority:** Should  
**Priority basis:** Multiple stakeholder documents and interviews state the need or recommend that the system provide missing/damaged reports per branch, in-transit reports per branch and system, a configurable in-transit-days threshold, and a merged transit-to/transit-from report; none of the sources use an explicit "must", so priority is inferred as Should.
**Sources:** DOC-005, DOC-010, DOC-015, DOC-018

### REQ-006 — Weeding / purging workflow: candidate identification, batch status conversion, last-copy detection, safe deletion and audit

Provide a Weeding/Purging workflow that: Customizable purge criteria (Must) supporting status-based conditions (e.g., missing, discard/weed, damaged), time-based conditions (in a status for X months/years), activity-based conditions (last circulated X days/months/years) and the ability to combine those conditions (for example: status = missing for >6 months AND no circulation in 2 years); read-only reports that list purge candidates prior to any change (Should); a batch status-conversion report/capability to change item statuses in bulk to support large changes (e.g., convert 100 items from 'missing' to 'discard/weed') (Should); a Last-Copy report (Must) that, for a chosen scope (library or system), identifies whether each item record is the only copy in that scope; a quick deletion mechanism (Should) to delete volume entries together with their copy entries and to remove bibliographic/item records that have no items attached; a separate confirmation step (Must) required before performing actual deletions; and an audit trail (Must) that records all purge and deletion actions, actors, timestamps and summary outcomes.

**Priority:** Must  
**Priority basis:** Overall Must; explicit subfeature priorities: Last copy report: Must (DOC-006)
**Sources:** DOC-006, DOC-010, DOC-015

### REQ-007 — Deletion audit logging and deletion reports (who/when/type/location; attempted/denied deletions)

Deletion audit logging and reporting — The system must count and track all record deletions (e.g., item records, patron records) and produce per-location and per-system deletion counts and reports; every deletion audit entry must record the record type, deletion timestamp, the user who performed the deletion, and the user's location; the audit must also record attempted and denied deletion operations (including who attempted the action, when, the record type and relevant location, and that the deletion was denied) to support compliance and troubleshooting.

**Priority:** Must  
**Priority basis:** Multiple source requests in conversations and early SRS documents ask explicitly for counting/tracking deletions per location and system and logging record type, timestamp, deleting user and user location, plus tracking denied attempts; that recurring request supports Must priority.
**Sources:** DOC-007, DOC-010, DOC-015

### REQ-008 — Patron demographics: configurable fields, grouping, filtering and null handling

Provide a configurable patron-demographics reporting capability that lets users select which demographic fields to include (at minimum: age range—with ranges configurable per report—ZIP code, county of residence, home branch, patron type, and preferred language), apply filters (LIMIT) and aggregate/group results (GROUP BY) on any of those fields, combine filters using AND/OR logic, include null/missing values as selectable filter and grouping outcomes, and produce demographic statistics (for example transactions by geographic region and by configurable age ranges) to support program planning and reporting.

**Priority:** Should  
**Priority basis:** Requested across multiple source documents (conversation notes, early SRS draft, and meeting minutes) with no explicit source priorities provided, so medium priority is inferred.
**Sources:** DOC-008, DOC-010, DOC-018

### REQ-009 — Inactive-patron reporting (configurable X days, include electronic activity types, hierarchical scopes, exclusions, export, background processing)

Inactive Patrons Report: The system must generate a list of patrons with no circulation or electronic activity in the last X days (X configurable); electronic activity must include logging into the OPAC or patron account, placing holds online, and renewing items online; the report must be configurable to run and be filtered at hierarchical scopes (System, Home Library, County, etc.); the report should allow exclusion of specified patrons from results; the report should produce or mark a separate subset of inactive patrons who still owe fines; the report should include each patron's current mailing address; the report should be exportable; and the report should execute as a background job and cache results to improve performance.

**Priority:** Must  
**Priority basis:** The core request explicitly requires generating the inactive-patrons list and that X be configurable, and supporting requests explicitly call for inclusion of specific electronic activity types, hierarchical scope configuration, exclusions, separate handling of patrons with fines, inclusion of current mailing addresses, exportability, and background processing with caching; where language used 'should' those subfeatures were treated as medium-priority requests and core list generation and X configurability were treated as high-priority.
**Sources:** DOC-009, DOC-010

### REQ-010 — Platform, architecture, accessibility, environments and separation (OS/db/browser/accessibility, standards HTML, dev/training migration, OPAC separation, read-only replicas)

Platform, Architecture, Accessibility and Environments — The system must support a large library consortium (286 locations, ~17,000,000 annual circulations, and purchasing/processing >900,000 items/year) and operate on Linux or Solaris server environments (including secondary sites such as Solaris 10 on SPARC for DR/reporting); use a fully relational database back-end compatible with relational schemas (including existing PostgreSQL 8.3 deployments) and permit read-only reporting replicas so reporting does not constrain the OPAC; be accessible via a web browser or a Windows-compatible client (if web-based, support Microsoft Internet Explorer 6.0+ and Mozilla Firefox 2.0+), produce standards-compliant, properly structured HTML (semantic markup, alt attributes, ARIA where appropriate), and be usable with assistive technologies (screen readers, screen-magnification and similar tools) to meet accessibility obligations; provide role/group-based access control for individuals, workgroups and arbitrary staff groups; include separate development/training environments that are safe for experimentation, support export/import or migration of configurations (report templates, permission settings and similar) to production, and ensure configuration migration and training activities do not risk production data or OPAC availability.

**Priority:** Must  
**Priority basis:** Overall Must; explicit subfeature priorities: Support for Library Consortium: Must (DOC-010); Linux or Solaris Server Support: Must (DOC-010); Web Browser Accessibility: Must (DOC-010); Web-Browser Compatibility: Should (DOC-010); Assistive Technology Compatibility: Must (DOC-010); Relational Database Requirement: Must (DOC-010); Standards-Compliant HTML: Must (DOC-010); Development Environment: Should (DOC-010); User Rights Control: Must (DOC-010)
**Sources:** DOC-010, DOC-014, DOC-016, DOC-018, DOC-019

### REQ-011 — Staff authentication and role-based access (card-swipe optional, username/password fallback, track staff identity, easy role administration)

Staff authentication and role-based access: The system must track which staff member is logged in for audit purposes (Must); it should support optional streamlined login methods (e.g., card swipe) but must not require them so branches lacking that infrastructure can operate (Should); it should provide a username/password fallback for staff without ID cards (Should); user rights and privileges should be managed through security groups/roles with access assignable to individuals, workgroups, and arbitrary staff groups (Should); changing a person’s permissions should be accomplished by changing their role assignment rather than editing individual permissions, and the system should make role administration straightforward and easy to perform (Should).

**Priority:** Must  
**Priority basis:** One source explicitly requires tracking the logged-in staff member (explicit "must"); other behaviors are described as supported or recommended ("should"/support), so the highest explicit priority is Must.
**Sources:** DOC-010, DOC-013

### REQ-012 — Query building, saved queries, query-reuse and query-selection display (user-friendly builder, save/reuse, show selection criteria alongside results)

The system should provide a user-friendly query builder for designing queries across all record types, allow users to save queries for repeated use and to reopen/re-run saved queries, and display the query selection criteria used to generate each result set alongside those results so users can see what criteria produced the report.

**Priority:** Should  
**Priority basis:** Multiple requirements documents and emails state the interface "should" (or "need") to support a user-friendly query tool and to display query selections with results; a survey explicitly prioritized the ability to save and reuse queries (73%), so the overall inferred priority is Medium (Should).
**Sources:** DOC-004, DOC-010, DOC-012, DOC-020

### REQ-013 — Report execution, queuing, scheduling, prioritization, cancellation, background processing, delivery and status visibility (position, status, prioritization, email/delivery/export)

Report Queueing and Delivery: The system shall provide queue visibility showing a user’s report position and how many reports are ahead, real‑time status indicators (waiting, running, completed, failed), background queuing and processing that allows reports to run during open hours without disrupting other system functions or slowing the circulation client, the ability to schedule recurring reports, the ability to cancel a scheduled or running report, support for report prioritization so high‑priority items (for example, a director’s board report) can be advanced ahead of ad‑hoc queries, and delivery support including email delivery of reports; users must be able to view position, status and prioritization for their reports and receive delivered reports by email.

**Priority:** Must  
**Priority basis:** Must: queue visibility and position/how many ahead (multiple requests; 68% survey), status indicators (explicit request), and background queuing/processing to avoid disruption and allow open‑hours processing (sysadmin interview). Should: schedule recurring reports (52% survey) and cancel scheduled or running reports (survey responses and technical feasibility). Should: report prioritization to allow critical reports to jump ahead (explicit request). Could: email delivery (45% survey). Overall priority set to the highest explicit subfeature priority (Must).
**Sources:** DOC-010, DOC-012, DOC-014, DOC-016, DOC-018, DOC-019, DOC-020

### REQ-014 — Data quality, validation rules and MARC/metadata extraction for quality reports (invalid item types, long call numbers, bibs with no items, last-circulation indicators)

The system Must generate data-quality reports that identify items with invalid item types, items with call numbers longer than configured thresholds (long call numbers), and bibliographic records with no associated item records; the system Must include a per-item last-circulation indicator on item reports and Must ensure the check-in date/time used for that indicator excludes renewals; the system Should extract the required MARC/metadata (for example: item-type fields, call-number fields, bibliographic-to-item linkage fields, and circulation history/checkin fields) to support the validation rules and populate the reports.

**Priority:** Must  
**Priority basis:** Inferred from multiple requests in the supplied documents calling for data quality reports (invalid item types, long call numbers, bibs with no items) plus explicit requests to indicate last circulation date and to exclude renewals from check-in timestamps.
**Sources:** DOC-015, DOC-018, DOC-020

### REQ-015 — Report output formats, presentation and exports (CSV/Excel/HTML, pivot/table output, include nulls; survey-name filtering)

Report output formats, presentation and exports: The system must provide export options in Excel, CSV and HTML formats, support scheduling of report generation/exports, include all nulls and blank fields in exported and presented results, and allow users to filter reports by survey name (the system must resolve survey names to the corresponding internal survey IDs when applying such filters).

**Priority:** Must  
**Priority basis:** Meeting notes and survey-response documents explicitly require Excel/CSV/HTML exports and inclusion of null/blank fields; a management/process reference requests multiple output formats and scheduling; meeting notes require survey-name filtering and internal name-to-ID resolution.
**Sources:** DOC-014, DOC-019, DOC-020

### REQ-016 — Transaction retention, archiving, privacy and financial audit trail (retention policy, archiving that protects patron privacy, snapshot bills/reporting over time)

Transaction Retention, Archiving and Privacy: The system must maintain an auditable financial trail by retaining and archiving transaction records and snapshot bills/reports over time according to a defined retention policy, ensure archived snapshots are discoverable for financial audit purposes, protect patron privacy by producing demographic statistics and any reporting output only in anonymized form with no personally identifiable information, separate reporting operations from production by providing a distinct reporting environment isolated from production operations, and provide a development/training environment with migration capability to move appropriate data and schemas between environments without exposing PII.

**Priority:** Must  
**Priority basis:** All candidates request core preservation, separation of reporting from production, a development/training environment with migration capability, and explicit anonymization of demographic statistics; these together indicate the feature is required rather than optional.
**Sources:** DOC-014, DOC-020

### REQ-017 — Financial and transaction reporting, value-of-items, auditing and retention (ledgers, payments, fines, retention policy enforcement, snapshot bills)

Must maintain a financial audit trail and compliance: Must maintain a ledger of patron payments that records which charges each payment is applied to to facilitate reconciliation, and must ensure all reports and archived financial data comply with standard accounting practice and state, county, and municipal auditing requirements and protect patron privacy per State Law. Should maintain transaction history for X days (X is configurable), enforce retention policies, and archive transactions in forms that protect patron privacy while permitting useful aggregated demographic statistics. Should attach fines, charges, waivers, and e-commerce transactions to both patron and item records; provide financial reports including patron account balances by patron, home library, and system; allow queries for patron accounts with balances greater than X dollars; produce snapshot bills reports that can show bills as of past points in time; and show payments broken down by payment method and by library (including fines waived per library). Should reflect payments immediately when made at the front desk to support up-to-date balances and reconciliation.

**Priority:** Must  
**Priority basis:** Multiple source statements explicitly use 'must' for ledger maintenance and legal/accounting compliance, while other requested behaviors are phrased as 'should' or 'need'; therefore the highest explicit priority is Must.
**Sources:** DOC-010, DOC-011, DOC-012, DOC-020

### REQ-018 — Uncataloged materials inventory and rapid low-effort processing

The system shall treat uncataloged materials (for example paperback books and children's board books) as inventory items even when not fully cataloged, provide lightweight, rapid processing and distribution workflows that minimize per‑item branch labor and enable quick turnaround, capture basic usage metadata to identify how uncataloged items are being used, and record transactions for those items so they are counted in circulation statistics and included in circulation reports.

**Priority:** Must  
**Priority basis:** Inferred Must for inventory control, tracking and rapid/low‑effort processing based on SRS mention of uncataloged material control and interview statements: “We need to be able to track these as inventory,” “We need to process these fast,” and “We can't spend a lot of time per item.” Counting transactions and including them in circulation statistics/reports and capturing usage are supported by interview requests to identify usage and include transactions in circulation statistics (inferred as high priority but slightly lower operational priority than immediate processing/tracking).
**Sources:** DOC-010, DOC-015

### REQ-019 — Online help, documentation and error reporting (data dictionaries, process descriptions, contextual help, meaningful errors)

Online help, documentation, and error reporting: The developer must provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and any other records maintained or accessed by Management Processes (Must); the developer should provide a thorough high-level description of major processes, including bibliographic record import and export, validation of bibliographic records against internal and external authority sources, and standard reports (Should); the system must provide an online, hierarchical, cross-linked HTML help system that describes and illustrates all system functions and is searchable and easy to navigate (Must, with searchable/navigation as a lower-priority usability request—Could); and the system should provide thorough high-level error reporting and feedback and allow low-level, query-specific feedback for Local and Global System Administrators accessible from the front-end interface (Should).

**Priority:** Must  
**Priority basis:** Overall Must; explicit subfeature priorities: Data Specifications Provision: Must (DOC-010); High-Level Description of Processes: Should (DOC-010); Online Help System: Must (DOC-010); Error Reporting and Feedback: Should (DOC-010)
**Sources:** DOC-010, DOC-016, DOC-018, DOC-019

### REQ-020 — Program governance and testing (working group responsibilities, templates testing)

The Reports working group must document optimal Reports functionality for future Evergreen releases and develop a clear list of requirements, and must serve as the official Reports testing group through which all new Reports development is filtered for validation and acceptance.

**Priority:** Must  
**Priority basis:** Both supporting candidates request that the group document Reports functionality/requirements and act as the Reports testing/filtering group; no explicit source priority was provided, so Must is inferred to ensure these governance and testing responsibilities are enforced.
**Sources:** DOC-017

### REQ-021 — Miscellaneous periodic/standard report types (cataloging, circulation, holds example reports)

Miscellaneous Periodic/Standard Reports: Provide support for periodic and standard report types for cataloging, circulation, and holds use cases, including at least the examples requested — a report of bibliographic records with holds and a report of items that have not been checked out in X days (where X is a configurable threshold); these report types must be capable of being scheduled and run on a recurring/periodic cadence and produced as distinct miscellaneous/standard report templates for operational use.

**Priority:** Should  
**Priority basis:** Inferred from the single requested example list of periodic reports (cataloging/circulation/holds) in the source; no explicit priority was provided, so a medium-level priority (Should) is inferred.
**Sources:** DOC-010

### REQ-022 — Report templates, cloning and fine-grained report permissions (admin-created templates, clone, role-driven permission changes)

Administrators must be able to create and manage report templates (including pre-defined/canned templates for boards, executives and for PINES libraries) that staff can access; templates must be clonable so a new template/report can be created from an existing one; the system must provide distinct, fine-grained, role- or security-group-based permissions that control who can create, clone, run and manage templates and reports; changing a user’s role assignment must automatically update that user’s report-related permissions to match the role; and the reporting subsystem must support the canned report definitions and fine-grained reporting requirements described in the referenced specifications and examples.

**Priority:** Must  
**Priority basis:** Some sources explicitly state the system 'must' support canned report definitions and fine-grained reporting requirements; other sources and a survey express strong need for admin-created templates, cloning, fine-grained permissions and role-based permission updates.
**Sources:** DOC-010, DOC-012, DOC-014, DOC-016, DOC-017, DOC-018, DOC-019, DOC-020

### REQ-023 — Backroom / circulation statistics (grouping by hour/terminal/branch/system, check-in/out type breakdowns, holds origin, transactions per-scope reports)

Backroom / circulation statistics: The system must provide transaction and backroom statistics that group transactions by hour, terminal, branch, and system; count check-ins both individually and cumulatively with check-in methods broken down at least into book drop, terminal/public terminal, and self-service; count check-outs both individually and cumulatively with distinct categories including staff checkout, self checkout, staff renewal, self checkout renewal, online renewal, and OPAC renewal; count all hold requests and record how each hold was placed (origin categorized as staff desk, public computer, or placed remotely) and report holds placed and holds filled; generate transaction reports (holds placed, holds filled, and check-outs) scoped per patron, per library, per selected group of libraries, per system, and per county; and support creation and reuse of report templates.

**Priority:** Must  
**Priority basis:** Multiple requests in DOC-010 (backroom statistics SRS) and DOC-020 (survey responses) explicitly ask for grouping by hour/terminal/branch/system, detailed check-in and check-out type breakdowns, holds origin reporting, transactions scoped by patron/library/group/system/county, and the ability to create report templates, so priority is inferred as Must.
**Sources:** DOC-010, DOC-020

### REQ-024 — Patron behavior analytics and prediction (statistics to understand/predict patron behavior; renew likelihood)

Patron Behavior Analytics and Prediction: The system should produce statistics and analytical outputs to enable understanding and prediction of patron behavior and use of materials, and should include item-level predictions of the likelihood that a borrowed item will be renewed so stakeholders can assess renewal risk and usage patterns.

**Priority:** Should  
**Priority basis:** Both source documents explicitly request production of statistics to understand and predict patron behavior and to predict renewal likelihood; neither assigns a priority, so a medium priority (Should) is inferred.
**Sources:** DOC-010, DOC-020

## Blacklisted requirements

- **Existing-system description: management-group / process background items:** Existing-system description, not a requested constraint: background about group activities, scope, and administration (meeting notes, project process descriptions) (sources: DOC-017)
- **Existing-system description: help / reporting environment notes (background):** Existing-system description, not a requested constraint: other background notes about reporting separation and environment (sources: DOC-019)
- **Concern about interface crowding:** Existing-system description, not a requested constraint: One consideration: with 286 locations, the overview might get crowded. (sources: DOC-002)
- **Shelf Space Estimation:** Existing-system description, not a requested constraint: The tricky part is #3. Shelf space isn't directly tracked in the database. (sources: DOC-003)
- **Existing transfer limitations:** Existing-system description, not a requested constraint: Currently no hourly scheduling. (sources: DOC-004)
- **Existing System Tracking for Missing Items:** Existing-system description, not a requested constraint: The system currently tracks item status as 'missing' or 'long overdue' or various other statuses. (sources: DOC-005)
- **Existing System Lacks Hourly Scheduling Feature:** Existing-system description, not a requested constraint: Currently no hourly scheduling. (sources: DOC-005)
- **Current lack of deletion tracking:** Existing-system description, not a requested constraint: Currently, Evergreen does not log deletions - once something is deleted, it's gone. (sources: DOC-007)
- **Non-required patron data availability:** Existing-system description, not a requested constraint: Some of these fields might not be consistently populated. (sources: DOC-008)
- **Canned Reports Types Listing:** Existing-system description, not a requested constraint: 14. APPENDIX A - REPORT TYPES This appendix lists the various report categories and example report types that have been identified as necessary. (sources: DOC-010)
- **Reporting Interface Requirements:** Existing-system description, not a requested constraint: 15. FINE-GRAINED REPORTING REQUIREMENTS This appendix contains detailed requirements for the reporting interface and functionality. (sources: DOC-010)
- **Existing limitation on hourly scheduling:** Existing-system description, not a requested constraint: Currently no hourly scheduling. (sources: DOC-011)
- **No Boolean operators in report writer:** Existing-system description, not a requested constraint: Limitations: No Boolean operators (AND/OR) beyond simple filters (sources: DOC-014)
- **Limited field selection in report writer:** Existing-system description, not a requested constraint: Limitations: Limited field selection (not all database fields are available) (sources: DOC-014)
- **No historical reporting warehouse:** Existing-system description, not a requested constraint: 4.2 MISSING FEATURES: No historical reporting warehouse (sources: DOC-014)
- **No ability to select Run ASAP:** Existing-system description, not a requested constraint: 4.2 MISSING FEATURES: No ability to select Run ASAP, Hourly, Daily, Weekly, Monthly, Yearly (sources: DOC-014)
- **No email delivery of reports:** Existing-system description, not a requested constraint: 4.2 MISSING FEATURES: No email delivery of reports (sources: DOC-014)
- **Need report template management system:** Existing-system description, not a requested constraint: 4.3 MISSING ARCHITECTURAL ELEMENTS: No report template management system (sources: DOC-014)
- **No accessibility support for report interface:** Existing-system description, not a requested constraint: 4.3 MISSING ARCHITECTURAL ELEMENTS: No accessibility support for report interface (sources: DOC-014)
- **Current system combines edit and circulation dates:** Existing-system description, not a requested constraint: The current system combines these dates. (sources: DOC-015)
- **Existing server specifications:** Existing-system description, not a requested constraint: Our main server is a Red Hat Enterprise Linux 5 box with dual quad-core processors and 32GB of RAM. (sources: DOC-016)
- **Current database version:** Existing-system description, not a requested constraint: It runs PostgreSQL 8.3 for the database. (sources: DOC-016)
- **Existing browser support issues:** Existing-system description, not a requested constraint: IE 6 is still common in our environment - I know it's old, but upgrading browsers on 200+ library computers is expensive and time-consuming. (sources: DOC-016)
- **Current user permission levels:** Existing-system description, not a requested constraint: PINES uses a role-based system. (sources: DOC-016)
- **Scope of working group:** Existing-system description, not a requested constraint: The group would focus on Management Processes - that is, reports and analysis tools used by library managers, administrators, and staff for planning, evaluation, and oversight purposes. (sources: DOC-017)
- **Exclusion of patron-facing functions:** Existing-system description, not a requested constraint: This does NOT include day-to-day patron-facing functions. (sources: DOC-017, DOC-018)
- **User interface specification:** Existing-system description, not a requested constraint: The group agreed to specify only those requirements that directly or indirectly relate to management activities. (sources: DOC-017)
- **Functional requirements focus:** Existing-system description, not a requested constraint: for now the focus should be on functional requirements. (sources: DOC-017)
- **Prototyping method:** Existing-system description, not a requested constraint: UI and data structures would require further specification using an iterative, prototype-oriented methodology. (sources: DOC-017)
- **integration with enterprise Library Automation System:** Existing-system description, not a requested constraint: Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System (sources: DOC-018)
- **consolidation at central location:** Existing-system description, not a requested constraint: Management Processes are consolidated at a central location, and accept input and provide services to multiple locations (sources: DOC-018)
- **dependence on external vendor websites:** Existing-system description, not a requested constraint: Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files (sources: DOC-018)
- **interaction with patron interface:** Existing-system description, not a requested constraint: Management Processes interact with a patron interface, also known as an Online Public Access Catalog (OPAC) (sources: DOC-018)
- **Central Consolidation Dependency:** Existing-system description, not a requested constraint: Management Processes are consolidated at a central location, and accept input and provide services to multiple locations. (sources: DOC-019)
- **Library Automation Dependencies:** Existing-system description, not a requested constraint: Management Processes rely on the data structures and functionality of an enterprise-level Library Automation System, including Acquisitions and Cataloging modules. (sources: DOC-019)
- **Vendor Integration Dependency:** Existing-system description, not a requested constraint: Management Processes interface with a variety of vendor websites, via published APIs and/or automated transfer of standard-format data files. (sources: DOC-019)
- **OPAC Interaction Dependency:** Existing-system description, not a requested constraint: Management Processes interact with a patron interface (OPAC). (sources: DOC-010, DOC-019)
- **Reports take too long to run:** Existing-system description, not a requested constraint: Reports take too long to run during busy hours. (sources: DOC-020)
- **Report processing visibility:** Existing-system description, not a requested constraint: I can't see if my report is still processing. (sources: DOC-020)
- **Confusing interface:** Existing-system description, not a requested constraint: The interface is confusing - I can't find the reports I need. (sources: DOC-020)
- **Excel export duplications:** Existing-system description, not a requested constraint: I need to export to Excel but the data has too many duplicate rows. (sources: DOC-020)
- **Field filtering availability:** Existing-system description, not a requested constraint: Can't filter by some fields that should be available. (sources: DOC-020)
- **MARC fields spread across rows:** Existing-system description, not a requested constraint: Need to pull specific MARC fields but they're spread across multiple rows. (sources: DOC-020)
- **Patron Privacy Requirement:** Existing-system description, not a requested constraint: but patron privacy means we can't keep personally identifiable information. (sources: DOC-012)
- **Enterprise-Level System Dependency:** Existing-system description, not a requested constraint: Management Processes are part of an enterprise-level Library Automation System. (sources: DOC-019)
- **Transaction Data Retention:** Existing-system description, not a requested constraint: State law requires us to retain transaction data for X years. (sources: DOC-012)
- **Current difficulties with login process:** Existing-system description, not a requested constraint: Currently, staff must type in their full username and password each time they sit down. (sources: DOC-013)
- **Service slowdown due to login:** Existing-system description, not a requested constraint: It slows down service - especially during busy periods, staff are spending precious seconds logging in instead of helping patrons. (sources: DOC-013)
- **Security issues from password sharing:** Existing-system description, not a requested constraint: It leads to security issues - staff get in a hurry and sometimes share passwords or leave terminals logged in. (sources: DOC-013)
- **No real-time reporting:** Existing-system description, not a requested constraint: 4.2 MISSING FEATURES: No real-time reporting (all reports are run on current data) (sources: DOC-014)
- **No report queue visibility:** Existing-system description, not a requested constraint: 4.2 MISSING FEATURES: No report queue visibility (staff can't see where their report is in queue) (sources: DOC-014)

## Open questions

- Which export formats (CSV, Excel, PDF, etc.) are required? (sources: DOC-009, DOC-010)
- How should exclusions be specified (individual patron IDs, patron groups, or rule-based criteria)? (sources: DOC-009, DOC-010)
- What background schedule or cache freshness policy is desired (e.g., run daily, weekly, or on demand)? (sources: DOC-009, DOC-010)
- What output formats and delivery schedule are required for the reports (e.g., CSV/JSON/PDF, ad hoc vs. nightly/weekly)? (sources: DOC-015, DOC-018, DOC-020)
- What exact threshold(s) define a 'long' call number (character count or configurable rule) and should thresholds be configurable per location/collection? (sources: DOC-015, DOC-018, DOC-020)
- Which MARC fields and schema/version must be extracted for each required element (item type, call number, bib-item link, circulation/checkin history) or should the extractor infer fields automatically? (sources: DOC-015, DOC-018, DOC-020)
- What specific retention periods or regulatory retention requirements must the retention policy meet (e.g., years, event-based triggers)? (sources: DOC-014, DOC-020)
- What standards or techniques define acceptable anonymization (e.g., de-identification, k-anonymity) and are there allowable minimal data fields for aggregated reporting? (sources: DOC-014, DOC-020)
- What scope and direction should the migration capability support between environments (e.g., production to training, training to production, full vs subsetted data), and are there restrictions on which data may be migrated? (sources: DOC-014, DOC-020)
- What output formats (reports, dashboards, CSV, API) and update frequency (real-time, daily, weekly) are required for the statistics and renewal predictions? (sources: DOC-010, DOC-020)
- Are there any data retention, privacy, or anonymization constraints that must apply to the behavioral data used for these analytics? (sources: DOC-010, DOC-020)
- Should categories/breakdowns in material-volume reports be fully customizable, and what degree of customization is required? (DOC-001)
- What specific metrics should be used to define 'capacity' for branch capacity interface (e.g., item count, shelf space, percent fullness, seating)? (DOC-002)
- Should date-range filtering be supported for which reports and at what granularities (point-in-time, inclusive ranges, snapshot-by-date)? (DOC-003)
- Should reports show nulls for missing demographic/patron data or exclude those records by default (policy choice)? (DOC-008)
- What specifically counts as 'electronic activity' for the inactive-patrons report (e.g., OPAC login, holds, renewals, e-resource access)? (DOC-009)
- Should we flag patrons who are inactive but still owe fines (binary yes/no), and what business rules determine this flagging? (DOC-009)
- Should the inactive-patrons report support fully open customization of the inactivity window (any number of days), or a set of predefined options? (DOC-009)
- Does Open Template Reporting exist or should it be specified as a required capability (clarify whether this is a gap or a known missing feature)? (DOC-014)
- Should the in-transit/missing item report support sorting by due date (and if so is due date the primary default)? (DOC-005)
- Should missing/damaged/in-transit reports include free-text item condition notes (e.g., 'water damage', 'vandalism') and if so from which field(s)? (DOC-005)
- Should the purging utility support automated scheduling (recurrence) and, if yes, what scheduling options/recurrence patterns are required? (DOC-006)
- Saved-query sharing policy and metadata: must saved queries support sharing between users and expose last-edit metadata (who/when)? (DOC-015)
- How should the system support both real-time operational reporting and historical, point-in-time (warehouse/snapshot) reporting? (If both, define expected report types per behavior, acceptable latency, and any separate architectures.) (DOC-019, DOC-020)

## Source documents

- **DOC-001:** `conversations\conv_pines014_material_volume.eml`
- **DOC-002:** `conversations\conv_pines015_capacity_interface.eml`
- **DOC-003:** `conversations\conv_pines016_shelf_space.eml`
- **DOC-004:** `conversations\conv_pines018_item_transfer.eml`
- **DOC-005:** `conversations\conv_pines019_020_missing_intransit.eml`
- **DOC-006:** `conversations\conv_pines021_item_purging.eml`
- **DOC-007:** `conversations\conv_pines022_deletions.eml`
- **DOC-008:** `conversations\conv_pines023_patron_characteristics.eml`
- **DOC-009:** `conversations\conv_pines024_inactive_patrons.eml`
- **DOC-010:** `early_draft_srs_galecia.txt`
- **DOC-011:** `email_financial_reports.eml`
- **DOC-012:** `email_report_features.eml`
- **DOC-013:** `email_staff_login.eml`
- **DOC-014:** `evergreen_reference_2009.txt`
- **DOC-015:** `interview_cataloging_2009-05-08.txt`
- **DOC-016:** `interview_sysadmin_2009-05-10.txt`
- **DOC-017:** `meeting_minutes\meeting_2009-03-15_minutes.txt`
- **DOC-018:** `meeting_minutes\meeting_2009-07-20_minutes.txt`
- **DOC-019:** `meeting_tech_subcommittee_2009-06-30.txt`
- **DOC-020:** `survey_results_2009.txt`
