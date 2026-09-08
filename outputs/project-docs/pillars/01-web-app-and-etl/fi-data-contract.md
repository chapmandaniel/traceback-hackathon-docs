# FI Data Contract

**Status:** Planning baseline — implementation not yet verified

[Pillar overview](README.md) · [Project home](../../README.md) · [Web experience](web-experience.md) · [ETL and lineage](etl-and-lineage.md)

## Purpose and fixture boundary

Define a fictional FI export that resembles information used by an AML SaaS while remaining small enough to implement and explain. This is our POC contract, not a universal AML standard or a vendor API replica. Required fields are requirements of this fixture.

Use `FI_DEMO_001`, a fictional retail and small-business bank. Start with 30 customers—24 individuals and six businesses—42 accounts, 46 holder links including four joint accounts, and approximately 1,000 posted external payments over 30 days. Generate reproducible, invented identities and references from a fixed seed. Volume can shrink before relationships or provenance are simplified.

The core currency is USD. Country, nationality, bank location, and currency are distinct concepts; USD does not establish a regulatory jurisdiction. Include salary receipts, ordinary bill payments, and business supplier payments. Defer internal transfers, reversals, foreign-exchange calculations, identity-document scans, screening results, and beneficial-owner resolution.

## Delivery package and parsing

Each isolated fixture has a manifest and four UTF-8 CSV files:

| File | Source namespace | Meaning |
|---|---|---|
| `customers.csv` | `CIF` | Customer master and selected FI-provided profile attributes |
| `accounts.csv` | `CORE` | Accounts and product attributes |
| `account_parties.csv` | Explicit on both linked references | Account holders, including joint ownership |
| `transactions.csv` | `CORE` | External payment postings against an FI account |

The manifest records FI, export time, file identities, checksums, expected counts, source systems, feed modes, and applicable contract versions. It is our ingestion wrapper. The importer records which mapping actually executed.

Treat customer, account, and relationship files as complete snapshots and payments as a declared time window. Initialize each scenario in its own fixture namespace; general incremental synchronization is deferred. Preview runs retain the original scenario identity and refer to its immutable source snapshot.

Use a header row and documented CSV quoting. Empty optional cells become null. Record logical data-row positions, starting at one after the header, without confusing them with physical lines in quoted CSV. Preserve original bytes. IDs are case-sensitive text; retain leading zeros and reject malformed identifiers rather than guessing. Date-only fields use `YYYY-MM-DD`; timestamps carry an explicit offset.

## Source fields

**R:** Required. **C:** Required for the specified customer type. **O:** Optional. FI and record source-system context may be inherited from the manifest.

### Customers

| Field | Need | Meaning |
|---|---|---|
| `customer_id` | R | Stable textual source identifier |
| `customer_type` | R | `P` individual or `B` business |
| `given_name`, `family_name` | C: individual | Supplied name components |
| `date_of_birth` | C: individual | Date-only birth date |
| `residence_country` | C: individual | Residence country, distinct from nationality |
| `legal_name` | C: business | Registered business name |
| `registration_number`, `registration_country` | C: business | Synthetic registration reference and jurisdiction |
| `incorporation_date` | O: business | Date-only incorporation date |
| `address_line_1`, `city`, `region`, `postal_code`, `address_country` | O | Residential address for a person; registered address for a business |
| `customer_status`, `customer_since` | R | `ACTIVE`, `INACTIVE`, or `CLOSED`; relationship start date |
| `occupation` | O: individual | FI-supplied occupation description |
| `industry`, `business_activity` | O: business | Industry/activity; document the coding scheme if coded |
| `source_of_funds` | O | Declared context such as salary or business revenue |
| `kyc_status`, `kyc_last_reviewed_at` | O | FI-provided review status and timestamp |
| `fi_risk_rating` | O | Existing FI assessment with documented code meanings |
| `expected_monthly_amount`, `expected_activity_currency` | O | Declared monthly activity; decimal major units under the customer contract |
| `source_updated_at` | R | Source-system update timestamp |

For populated review fields, document fixture codes such as `REVIEW_COMPLETE` and `LOW` in the applicable customer contract. These are imported assertions. They are not decisions made by Traceback. Keep inapplicable attributes null; a business has no date of birth.

### Accounts

| Field | Need | Meaning |
|---|---|---|
| `account_id`, `account_reference` | R | Stable source ID and separate synthetic display reference |
| `product_code` | R | `CHK`, `SAV`, or `BUS_CHK` |
| `account_currency` | R | USD for the core fixture |
| `account_status`, `opened_date` | R | Documented status code and opening date |
| `closed_date` | O | Closing date when supplied |
| `account_purpose` | O | Personal banking or business operations, for example |
| `branch_reference` | O | FI branch reference; does not establish customer residence |
| `source_updated_at` | R | Source-system update timestamp |

Use `ACTIVE` or `CLOSED` for the initial account-status code list. Account balances are deferred because they require separate as-of and reconciliation semantics.

### Account holders

| Field | Need | Meaning |
|---|---|---|
| `account_source_system`, `account_id` | R | Exact account namespace and identifier |
| `customer_source_system`, `customer_id` | R | Exact customer namespace and identifier |
| `relationship_role` | R | `OWNER` or `JOINT_HOLDER` |
| `valid_from`, `valid_to` | O | Relationship validity dates when supplied |

An account may have several holders and a customer several accounts. Deduplicate transaction IDs when building a customer's transaction history. Account ownership does not establish ownership of a business. Authorized signers and beneficial owners would require separately typed relationships.

### Transactions

| Field | Need | Meaning |
|---|---|---|
| `transaction_id` | R | Unique posting reference within FI and source namespace |
| `account_source_system`, `account_id` | R | Referenced FI account |
| `occurred_at`, `posted_at` | R | Business and posting timestamps with offsets |
| `amount` | R | Positive integer string in minor units under the initial USD payment contract |
| `currency` | R | USD in the core fixture |
| `debit_credit` | R | `D` or `C`, relative to the FI account |
| `payment_type` | R | `EFT` or `WIRE` |
| `channel` | O | `WEB`, `MOBILE`, or `BRANCH` |
| `transaction_status` | R | `BOOKED` |
| `counterparty_name` | R | Other party named in the payment |
| `counterparty_account_reference` | O | Synthetic external reference |
| `counterparty_country` | O | Supplied address country of the other party |
| `counterparty_bank_country` | O | Country of the other party's bank |
| `payment_reference` | O | Remittance or invoice reference |
| `initiating_customer_id` | O | Known initiating customer in the documented `CIF` namespace |
| `source_updated_at` | R | Source update timestamp |

External counterparties need not appear in the FI customer master. Missing external account details must not erase a valid FI-account link. A debit is outbound and a credit inbound; keep amounts positive instead of encoding direction twice. Account holders are not necessarily the person who initiated a payment.

## Canonical mapping rules

| Source | Canonical treatment |
|---|---|
| Customer `P` / `B` | `INDIVIDUAL` / `BUSINESS` |
| Source identifiers | Resolve by FI, source system, object type, and text ID; retain separate internal keys |
| Payment `D` / `C` | `OUT` / `IN` relative to the linked account |
| Payment `125000`, applicable contract says USD cents | Exact major-unit decimal string `1250.00` with currency `USD` |
| Expected activity `4000.00` | Remains `4000.00`; the customer contract already specifies major units |
| `CHK` / `SAV` / `BUS_CHK` | `CHECKING` / `SAVINGS` / `BUSINESS_CHECKING` |
| Offset timestamp | Normalize the instant to UTC; retain source text |
| Date-only value | Preserve the calendar date without timezone conversion |
| Empty optional cell | Null; never silently zero, false, or low risk |

Use exact decimal arithmetic and decimal strings in monetary API values. Retain normalized payment amounts in major units so the missing conversion is an actual processing defect. The USD fixture's scale must not become an assumption that every currency uses two decimal places.

Unresolved relationships and duplicate transaction IDs within the fixture namespace produce recorded outcomes. They must not create guessed links or silently inflated totals. Detailed processing behavior belongs in [ETL and lineage](etl-and-lineage.md).

## Connected example

These JSON objects illustrate CSV rows; they are not an additional delivery format. Optional or inapplicable fields are omitted.

```json
{
  "customer_id": "000041",
  "customer_type": "P",
  "given_name": "Maya",
  "family_name": "Rowan",
  "date_of_birth": "1988-04-17",
  "residence_country": "US",
  "customer_status": "ACTIVE",
  "customer_since": "2022-06-10",
  "occupation": "Architect",
  "source_of_funds": "SALARY",
  "kyc_status": "REVIEW_COMPLETE",
  "fi_risk_rating": "LOW",
  "source_updated_at": "2026-08-31T18:00:00Z"
}
```

```json
{
  "account_id": "001234",
  "account_reference": "DEMO-ACCT-001234",
  "product_code": "CHK",
  "account_currency": "USD",
  "account_status": "ACTIVE",
  "opened_date": "2022-06-10",
  "source_updated_at": "2026-08-31T18:00:00Z"
}
```

```json
{
  "account_source_system": "CORE",
  "account_id": "001234",
  "customer_source_system": "CIF",
  "customer_id": "000041",
  "relationship_role": "OWNER"
}
```

```json
{
  "transaction_id": "PAY-000481",
  "account_source_system": "CORE",
  "account_id": "001234",
  "occurred_at": "2026-09-01T09:15:00-04:00",
  "posted_at": "2026-09-01T09:16:00-04:00",
  "amount": "125000",
  "currency": "USD",
  "debit_credit": "D",
  "payment_type": "EFT",
  "channel": "WEB",
  "transaction_status": "BOOKED",
  "counterparty_name": "Example Property Services",
  "counterparty_account_reference": "EXT-DEMO-8821",
  "counterparty_country": "US",
  "payment_reference": "RENT-SEP-2026",
  "source_updated_at": "2026-09-01T13:16:00Z"
}
```

The correct payment is USD 1,250.00 under `core-payment-v1`. A business row uses `customer_type=B`, `legal_name=Example Workshop LLC`, `registration_number=DEMO-REG-000006`, and `registration_country=US`, with its own required status, relationship date, and update time. It leaves person-only attributes empty.

## Evidence and published contract versions

Publish immutable customer, account, holder, and payment contract versions plus inspectable mapping logic for the knowledge pillar. The [shared interface contracts](../../shared/interface-contracts.md) define their cross-pillar references; do not invent parallel payload schemas here.

Source unit annotations must distinguish an authoritative contract declaration from an importer's assumption. The unknown control uses an unavailable applicable version without equivalent authoritative unit evidence elsewhere. Private fixture labels and expected answers never enter business records or knowledge retrieval.

## Reference basis

The categories were informed by these official vendor descriptions; our field names and requirements are fictional design choices:

- [ComplyAdvantage customer model](https://docs.mesh.complyadvantage.com/docs/customers): person/company profiles and supporting customer context.
- [Unit21 instruments](https://support.unit21.ai/hc/en-us/articles/7796557710356-Instruments): financial instruments separate from associated entities.
- [ComplyAdvantage batch transaction upload](https://support.complyadvantage.com/articles/5320269470-batch-transaction-upload): identifiers, time, money, channels, and participants.
- [Unit21 data integration guidance](https://support.unit21.ai/hc/en-us/articles/6433426083732-Best-Practices-when-sending-Data-to-Unit21): stable identifiers and relationships.

Readiness is assessed using [the canonical acceptance criteria](../../shared/acceptance-and-readiness.md).
