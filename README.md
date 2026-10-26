# undomesticatedai.com

Public source for **Undomesticated AI**, the founder/research surface of Garth Noel.

## Purpose

This repository is deliberately separate from ANANS runtime and research repositories.

Undomesticated AI is for public writing, research notes, architectural questions, selected experiments, failures worth exposing, and external pressure tests around increasingly capable machine systems.

ANANS may appear here as an ongoing research-and-build programme through which propositions are tested. This repository is **not** the ANANS codebase, governance authority, evidence store, or confidential research surface.

## Boundary

- No ANANS confidential material.
- No automatic publication from ANANS outputs.
- No runtime, model, agent, or generated artifact is publication authority.
- Claims about implemented systems should link to inspectable public evidence where available.
- Experimental or speculative material should remain labeled as such.
- Public writing here does not imply that ANANS is finished, externally validated, production-ready, or generally autonomous.

## Initial architecture

Static HTML on GitHub Pages. No framework, CMS, database, analytics dependency, or source coupling to ANANS is required for the initial surface.

Domain target: `undomesticatedai.com`

## CEA Lens development candidate

`lens/` adds browser-local, source-bound task preparation and structural receipt checking toward the ARMO trajectory. CEA v5 is selected canonical by Founder directive. The default registry holds until exact v5 and separately versioned taxonomy bytes are bound; no canonical text is reconstructed or published here.

Run `npm test` for deterministic synthetic conformance checks; `npm run dev` serves the local candidate. See [implementation and limits](docs/ARMO_PREPARATION.md). This branch does not connect to or execute ANANS runtime operations, admit candidates, call providers, merge or deploy itself.
