# Refined Software Requirements

## Priority scale

- **Must:** Essential for the system's core needs.
- **Should:** Important, but a reasonable first release can work without it.
- **Could:** Useful but optional.
- Priorities are estimates unless a source explicitly states them.

## Requirements

### REQ-001 — ConsortiumScaleSupport

The system must support operation at library-consortium scale (hundreds of locations, millions of annual circulations, and large annual acquisitions/processing volumes) so it can serve the size and load characteristics of the target consortium.

**Priority:** Must  
**Sources:** DOC-010, DOC-018

### REQ-002 — ServerEnvironment

The system must be deployable on the consortium's server platforms; specifically it must operate on Linux or Solaris server environments as required by operations staff.

**Priority:** Must  
**Sources:** DOC-010, DOC-018, DOC-016

### REQ-003 — RelationalDatabaseBackend

The system must use a fully relational database back-end compatible with the consortium's chosen RDBMS (PostgreSQL is the stated current choice) and work with the existing relational data structures.

**Priority:** Must  
**Sources:** DOC-010, DOC-018, DOC-019

### REQ-004 — AccessibilityCompliance

The system must meet accessibility requirements: produce standards-compliant, properly structured HTML and be compatible with assistive technologies (screen readers, magnifiers, ARIA/alt tagging, etc.), consistent with Section 508 and equivalent accessibility expectations.

**Priority:** Must  
**Sources:** DOC-010, DOC-016, DOC-019

### REQ-005 — OPACNonConstraint

Management/reporting processes must not constrain or negatively impact the functionality or features of the public Online Public Access Catalog (OPAC) module; reporting must be architected to avoid reducing OPAC capabilities.

**Priority:** Must  
**Sources:** DOC-010, DOC-016, DOC-019

### REQ-006 — DevelopmentAndTrainingEnvironment

The system must provide separate development and training environments and the ability to migrate configurations from those environments to production so staff can test and train without risking production data or workflows.

**Priority:** Must  
**Sources:** DOC-010, DOC-019, DOC-018

### REQ-007 — RoleBasedAccessControl

User rights and privileges must be managed via security groups and/or roles that allow access control for individuals, workgroups, and arbitrary staff groups; changing someone's permissions should be achievable by changing role assignments.

**Priority:** Must  
**Sources:** DOC-010, DOC-013, DOC-016, DOC-018, DOC-019

### REQ-008 — QueryAndReportEngine

The system must provide a user-friendly reporting/querying engine allowing staff to design queries and reports against all relevant record types (bibliographic, item, patron, transactions, etc.) and to run those reports against the system data.

**Priority:** Must  
**Sources:** DOC-010, DOC-012, DOC-014

### REQ-009 — BackgroundProcessingAndQueueVisibility

Reports must be able to be queued and processed in the background (to avoid disrupting operations) and the system must provide visibility into the report queue and report status (waiting, running, completed, failed) for submitters.

**Priority:** Must  
**Sources:** DOC-016, DOC-012, DOC-019, DOC-020

### REQ-010 — NonDisruptiveReporting

Reporting and query processing must be architected so searches and reports can be processed during open hours without disrupting other system functions (including OPAC), e.g., via background processing, replicas, or other isolation mechanisms.

**Priority:** Must  
**Sources:** DOC-016, DOC-019

### REQ-011 — OutputFormats

The system must support common export/output formats for reports, at minimum CSV and standards-compliant HTML, and should support Excel-compatible output where required by users.

**Priority:** Must  
**Sources:** DOC-014, DOC-019

### REQ-012 — IncludeNullsInResults

When returning/reporting records, the system must include null and blank fields in results rather than implicitly excluding them so that reports accurately reflect missing data.

**Priority:** Must  
**Sources:** DOC-008, DOC-019

### REQ-013 — ReportTemplatesAndAdminControl

System administrators must be able to create report templates that are available to staff; administrators must be able to restrict which filters and display fields in templates can be altered and provide templates that can be run as-is or modified safely.

**Priority:** Must  
**Sources:** DOC-010, DOC-012, DOC-020

### REQ-014 — FineGrainedReportPermissions

The system must provide distinct, fine-grained permission levels that control who can create, modify, clone, and run reports and templates; permission administration should be straightforward for administrators.

**Priority:** Must  
**Sources:** DOC-010, DOC-012, DOC-020

### REQ-015 — HelpSystem

The system must provide an online, hierarchical, cross-linked, searchable HTML help system that documents and illustrates system functions and is available to users from the front-end interface.

**Priority:** Must  
**Sources:** DOC-010, DOC-019, DOC-016

### REQ-016 — HTMLStandardsAndValidation

All web-based output must be standards-compliant HTML and should validate against W3C standards; HTML must be properly structured for accessibility (alt tags, ARIA where appropriate, semantic markup).

**Priority:** Must  
**Sources:** DOC-010, DOC-019, DOC-016

### REQ-017 — DeveloperDataSpecifications

The software developer must provide complete data specifications for authority records, bibliographic records, order records, item records, hold/request records, and other records maintained or accessed by management processes to enable reporting and integration.

**Priority:** Must  
**Sources:** DOC-010, DOC-019, DOC-018

### REQ-018 — AuditTrailForDeletionsAndReporting

The system must count and track deletions (item, patron, etc.) and record an audit trail that includes record type, timestamp, user performing the deletion, user location, and optionally denied deletion attempts; a report interface to query this audit table is required for auditing and compliance.

**Priority:** Must  
**Sources:** DOC-007, DOC-006, DOC-015

### REQ-019 — FinancialReportingAndLedger

The system must support financial reporting including patron account balances, fines/charges/waivers and payments by period and by branch, and must maintain a ledger of patron payments showing which charges payments were applied to to enable reconciliation and auditing.

**Priority:** Must  
**Sources:** DOC-011

### REQ-020 — TransactionArchivingAndPrivacy

Transactions must be archived in a way that protects patron privacy according to state law while preserving useful demographic statistics; retention and anonymization approaches must be provided to meet legal and reporting needs.

**Priority:** Must  
**Sources:** DOC-010, DOC-012, DOC-020

### REQ-021 — MaterialVolumeReport

The system must provide material-volume reporting for a chosen library or scope showing total item counts at a point in time, with date filters to view historical points in time and breakdowns by categories (with categories configurable per library), and counts should include checked-in items, checked-out items, and new acquisitions where applicable.

**Priority:** Must  
**Sources:** DOC-001, DOC-015

### REQ-022 — InTransitItemsReport

The system must generate an in-transit items report listing items in transit beyond a configurable threshold X days (X configurable, default suggested), with scope per branch or system; the report should merge transit-to and transit-from views and support sorting (e.g., by due date) and including condition notes where available.

**Priority:** Must  
**Sources:** DOC-005, DOC-015

### REQ-023 — MissingAndDamagedItemsReport

The system must provide reports of missing and damaged items per branch (and aggregated at system level) for auditing and collection decision purposes.

**Priority:** Must  
**Sources:** DOC-005, DOC-015

### REQ-024 — LastCopyReport

The system must provide a last-copy report that identifies a system's or library's last copies (the only copy within the specified scope) to prevent accidental deletion of unique holdings.

**Priority:** Must  
**Sources:** DOC-006, DOC-015

### REQ-025 — PurgingUtilityAndReports

The system should provide utilities and reports to identify candidate item records for purging based on customizable criteria (status-based, activity-based such as last-circulated timeframe, combinable criteria), present candidates in read-only reports, require a separate confirmation step for destructive deletions, and maintain an audit trail of purge activity to prevent accidental large-scale data loss.

**Priority:** Should  
**Sources:** DOC-006, DOC-015

### REQ-026 — ItemTransferUtility

The system should provide a utility for transferring batches of items between branches including the ability to query candidate materials, save queries for repeated use, manually select titles from query results, change item-location fields or generate pull lists to enact moves, preview changes before applying them, and limit transfer capability to authorized staff via permissions.

**Priority:** Should  
**Sources:** DOC-004, DOC-015, DOC-012

### REQ-027 — TransferUndoPreviewAndHistory

For item transfers the system should provide a preview of intended changes before committing, an undo function to revert mistaken changes, and a transfer history log; it should support reverting items automatically after specified conditions where defined (see separate revert requirements).

**Priority:** Should  
**Sources:** DOC-004, DOC-015

### REQ-028 — TransferAutoRevertByTimeAndEvent

The system should support reverting transferred items either after a specified time period (time-based revert) or in response to an event (e.g., when item status becomes 'returned'), where revert criteria are configurable.

**Priority:** Should  
**Sources:** DOC-004

### REQ-029 — TransferAuxiliaryFeatures

The transfer utility could provide auxiliary features such as generating transit labels and notifying staff of delayed or problematic transfers (alerts); these features are optional and should be considered for later releases.

**Priority:** Could  
**Sources:** DOC-004

### REQ-030 — ShelfSpaceUtilizationReports

The system should provide shelf-space utilization reports per genre/format that show percentage of total circulations, percentage of the collection, and percentage of total shelf space; reports should be runnable per library or system, support side-by-side comparison views across libraries, and allow date-range filtering. Because shelf space may not be directly tracked, the system should allow estimation using item dimensions or item counts as a proxy.

**Priority:** Should  
**Sources:** DOC-003, DOC-015, DOC-018

### REQ-031 — PatronCharacteristicsQueries

The system should allow queries and reports to be limited or grouped by patron characteristics (age range, zip code, county, home branch, patron type, preferred language), support both filtering (LIMIT) and grouping (GROUP BY) semantics, allow combining filters with AND/OR logic, include null values in results, and make age ranges configurable per report.

**Priority:** Should  
**Sources:** DOC-008, DOC-020

### REQ-032 — InactivePatronsReport

The system should provide an inactive-patrons report listing patrons with no circulation or electronic activity for a configurable number of days (X configurable), with configurable report scopes (system, home library, county), inclusion of mailing addresses for outreach, the ability to exclude specified patrons, differentiation for patrons with outstanding fines, exportability of results, and background processing/caching for performance.

**Priority:** Should  
**Sources:** DOC-009

### REQ-033 — ReadOnlyReportingReplicas

The system should support read-only reporting replicas or other mechanisms that offload reporting workloads from production to prevent disruption and to enable more extensive background processing and historical queries.

**Priority:** Should  
**Sources:** DOC-016, DOC-019

### REQ-034 — ReportSchedulingAndCancellation

The system should support scheduling reports to run at regular intervals (daily/weekly/monthly) and provide mechanisms to cancel scheduled or running reports; scheduling granularity and policies should be definable by administrators.

**Priority:** Should  
**Sources:** DOC-014, DOC-019, DOC-012

### REQ-035 — QueryFeatures

The reporting/query interface should allow staff to select fields to query, use picklists, support Boolean operators for combining filters, offer the ability to save and reuse queries, support cloning of reports/templates, and provide advanced matching options such as regular expressions where indicated.

**Priority:** Should  
**Sources:** DOC-012, DOC-014, DOC-020

### REQ-036 — ExecutiveAndCapacityDashboards

The system should provide executive-level interfaces that give high-level overviews of branch capacities (all branches at once) with drill-down into individual branches, filtering and sorting (region, type, load), trend display, and export options (e.g., CSV) while addressing scalability/crowding concerns for large numbers of locations.

**Priority:** Should  
**Sources:** DOC-002, DOC-018

### REQ-037 — DataQualityReports

The system should provide data-quality reports (e.g., items with invalid item type, long call numbers, bibliographic records with no attached item records) to assist cataloging and cleanup workflows.

**Priority:** Should  
**Sources:** DOC-015, DOC-018

### REQ-038 — ValueOfItemsReport

The system could provide reports computing the monetary value of items based on financial or item-record data so staff can get aggregate value information for inventories and insurance/audit purposes.

**Priority:** Could  
**Sources:** DOC-011

### REQ-039 — PredictiveAndDemographicStatistics

The system could produce demographic and predictive statistics (anonymized where required) to help understand and plan for patron behavior and program planning; these analytics are optional enhancements beyond core reporting.

**Priority:** Could  
**Sources:** DOC-020, DOC-018

## Blacklisted requirements

- **ComplexQueriesDifficulty (observational):** This candidate describes a limitation of an existing system (Evergreen) rather than stating a new functional requirement; it is commentary, not a requirement to be implemented as-is. (sources: DOC-014)
- **NoBooleanOperatorsSupport (observational):** This is an observation about a current product limitation, not a standalone requirement. Boolean operator support is captured as a proper requirement elsewhere (QueryFeatures). (sources: DOC-014)
- **NoEmailDelivery (observational):** This notes an existing product limitation (lack of email delivery) rather than defining a required feature. Email delivery is not requested explicitly as a required feature in the candidate set; treat it as out-of-scope observational evidence. (sources: DOC-014)
- **NoHourlyScheduling (observational):** This statement documents a current limitation (no hourly scheduling) rather than specifying a required behavior. Scheduling requirements are captured generally (scheduling supported), and granularity should be clarified via open question. (sources: DOC-014)

## Open questions

- What are the authoritative retention periods and retention policies for transaction history vs aggregated data (the candidates reference 'X days (configurable)', 'monthly/annual aggregates retained indefinitely', and 'some data needs to be retained for 7 years for audit purposes')? Clarify required default values and which data elements must be retained for specified statutory periods.
- Should the transfer auto-revert facility support arbitrary 'other criteria' beyond the documented time-based and event-based triggers? If so, what types of criteria must be supported and how should they be expressed (rule engine, set of predefined triggers)?
- Can the item-purging utility be scheduled to run automatically (fully scheduled purges), or must purging be manual with scheduled reporting only? The candidates include both a question about scheduling (uncertain) and requests for safe confirmation workflows.
- For the executive 'capacity' interface, what exact metric(s) define 'capacity' for each branch (e.g., physical shelf slots, percentage filled by collection, staff/seat capacity, processing load)? The design depends on the authoritative definition.
- Which web browsers and minimum versions must be supported for the first release? Candidates reference Microsoft Internet Explorer 6.0+ and Mozilla Firefox 2.0+, but these are historic; confirm current supported browser versions and mobile support expectations.

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
