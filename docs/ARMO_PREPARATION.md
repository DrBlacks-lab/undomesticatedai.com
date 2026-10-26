# CEA Lens: bounded ARMO preparation

State: implemented development candidate; local deterministic checks recorded separately. Not deployed or connected to the ANANS runtime. CEA v5 selection is settled by the 2026-10-26 Founder directive; its exact source bytes are not yet bound in this checkout.

This extends the existing September CEA Lens design, rather than creating another canonicality resolver or ARMO runtime. The existing public static site, identity registry and evidence pages remain the foundation. Existing ANANS custody/selector and independently namespaced taxonomy machinery must supply reviewed source bindings; this site does not replace or authenticate them.

## Implemented cut

`/lens/` imports exact UTF-8 CEA and taxonomy files locally, verifies their raw-byte SHA-256 against a selected registry, and compiles a self-contained JSON task capsule. The capsule binds run ID, request mode, source versions/digests, taxonomy namespace, worker/evaluator identifiers, zero-effect resource limits and subject data. It preserves a byte digest of the serialized capsule. It offers a response template and deterministic response-envelope checking against the current capsule and registry.

Registry replacements are operator-supplied input. A digest match is byte consistency, not proof of canonical custody, source authorship or release eligibility. `registry_object_sha256` hashes `JSON.stringify` of the parsed registry, including its insertion order; it is not a digest of the registry file's raw bytes or a signature. Any change to that serialized object invalidates a prior capsule. The browser is not a trusted admission boundary. A hostile client can alter the registry or the checker. Distinct role identifiers are only a structural separation check, not independent evaluation or actor authentication.

The default registry records the v5 choice and intentionally has null byte bindings, null taxonomy identity and null expiry. Compilation therefore holds. No older source, later draft or reconstructed CEA text is used as v5. There is no public `current` CEA pointer and no CEA source publication in this change.

## Run locally

Requires Node 20+ with WebCrypto; browser use requires WebCrypto and ES modules. No package installation or third-party dependencies are needed.

```sh
npm test
npm run dev
```

Open the printed local URL followed by `/lens/`. GitHub Pages remains the production architecture; the development server is not a production server.

## Reviewed source-binding interface

Use the existing custody and taxonomy mechanisms to produce a reviewed registry in the shape of `protocol/manifest-v1.json`. Only after exact source custody is reconciled:

- Keep `selection.cea_version` and `cea.version` equal to `v5`.
- Set `binding_status` to `BOUND`; supply CEA raw-byte SHA-256 and a meaningful source reference.
- Supply the separately selected taxonomy version, namespace, raw-byte SHA-256 and source reference. CEA version selection does not settle taxonomy numbering or the P6 collision.
- Set a new explicit registry revision and a future `valid_until` timestamp.
- Preserve `execution_enabled: false` and `authority_delta: 0`.

Import that reviewed registry and both exact local source files in the Lens. File contents remain in browser memory. Downloaded capsules contain the full source and subject text; review their disclosure scope before sharing. The source bytes need not be placed in the public repository to use local preparation.

This interface does not perform source admission and does not allow this application to mark its own output canonical.

## Review result meanings

| Result | Meaning |
| --- | --- |
| `HOLD` before compilation | Registry/source dependency unavailable, expired or mismatched. |
| `INVALID` | A structural, binding, role, resource or authority invariant failed. |
| `STRUCTURALLY_VALID_FOR_REVIEW` | Declared fields satisfy this checker against the current local capsule. Still not an admission decision. |

The review envelope's `admissibility` is a proposal made by its author. Even a well-formed `PASS` always yields `execution_authorized: false`. A consequential-action capsule cannot return `PASS`. A non-effectful next action can still be proposed. Empty adverse/missing arrays are permitted and never interpreted as proof that adverse evidence or unknowns do not exist.

Local build/test modes classify the requested task, but this page authorizes and executes no build or test. Any downstream work needs the existing operator mandate. The fixed zero-effect resource envelope applies to the reviewed preparation work. A model call made outside this page has its own authorization and cost receipt; this implementation makes no provider call.

No output parser can detect a lie in an unrestricted prose string. For example, an effect described in `analysis` can escape semantic detection even when the typed next-action field is constrained. Resource values and actor identifiers are self-reported. Duplicate-run rejection across sessions, signatures, semantic correctness, causal efficacy and independent reviewer judgment are not implemented here. A changed current capsule rejects an envelope from a different run; there is no global replay ledger.

## Validation ceiling

Tests use explicitly synthetic procedure/taxonomy bytes. They exercise raw-byte binding, UTF-8/BOM/CRLF preservation, source and capsule mismatches, run/context substitution, authority expansion, request classes, resource budgets and typed effect rejection. They do not test CEA v5 semantics or downstream model compliance.

This is a local unit/conformance run authored with the implementation. It is neither independent validation nor a held-out comparative efficacy assay. The September six-arm comparative protocol, evaluator freeze, anti-dampening measures, provider authority and actual task outcomes remain separate work. There is no AEL-attributable gain, autonomous RSI result or ARMO operational-readiness claim.

Browser QA in this session: the page layout and disabled compilation state rendered, but script startup remained at “Loading registry”; direct script navigation returned `ERR_BLOCKED_BY_CLIENT`. Cause is unresolved. Node tests exercise page-state handling with a minimal DOM adapter, which is not a browser validation substitute. Browser file import, compilation, download and returned-envelope checking remain unverified. This adverse result blocks release readiness.

## Next integration sequence

1. Bind exact CEA v5 and separately selected taxonomy through existing custody. Retain the selection directive independently from the source-byte receipt.
2. Validate the real-source capsule path and complete browser interaction checks. Preserve the current synthetic cases and any adverse results.
3. Freeze the existing comparative assay and independent evaluator before any authorized model trials. Evaluate false authorization, false holds, useful task completion, cost and failures.
4. Route reviewed candidates to existing ARMO/BOARD interfaces only through a separately reviewed adapter. Preserve their admission and execution boundaries; do not build another machine organization in this public site.
5. Release the public page only under the applicable publication mandate. Runtime connection, actuation, promotion and general autonomy are separate decisions.

## Provenance

- Repository base inspected: `1f8771cdb56b9d8e9402aca4ec0c4742a263f6a1`.
- Existing `UNDOMESTICATEDAI_CEA_LENS_OPTIMAL_DESIGN_V0_1.md` and `UNDOMESTICATEDAI_CEA_LENS_CONTRACT_V0_1.json` were read in full. Their old version-conflict fields are qualified by the current Founder selection of v5; missing byte custody remains missing.
- The later `ANANS_CEA_TAXONOMY_RECONCILIATION_20261012_V0_1.json` was read and its duplication/namespace warnings retained.
- A remote read of the known CEA folder returned v3.2 and v4.1 files, not v5. A broader filename search was terminated without output to bound resource use; this is not proof that v5 does not exist.
- Private CEA text, private runtime code, provider credentials and laptop content are not included in this change.
