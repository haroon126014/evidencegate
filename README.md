# EvidenceGate

EvidenceGate is a GenLayer Intelligent Contract for checking factual claims against a public source.

You give it:
- a claim
- an evidence URL

Validators read the source and return one of four results:
- `SUPPORTED`
- `CONTRADICTED`
- `INSUFFICIENT`
- `SOURCE_UNAVAILABLE`

The verdict and a short explanation are stored on-chain.

## Why I built it

Some on-chain workflows need to verify information that exists outside the chain.

This can be useful for:
- prediction market settlement
- milestone checks
- governance
- agent claims
- attestations

The goal was to keep the contract small enough to reuse in other apps.

## Contract flow

1. Create a claim with `create_claim`
2. Add a public evidence URL
3. Call `evaluate`
4. Validators inspect the source
5. GenLayer consensus decides the result
6. Read the verdict and reasoning from the contract

## Methods

Write:
- `create_claim(claim, evidence_url)`
- `evaluate()`

Read:
- `get_claim()`
- `get_evidence_url()`
- `get_verdict()`
- `get_reasoning()`
- `is_evaluated()`

## Consensus

The contract uses:
- `gl.nondet.web.render`
- `gl.nondet.exec_prompt`
- `gl.eq_principle.prompt_comparative`

The verdict has to match exactly between equivalent validator outputs. Reasoning can be worded differently as long as it supports the same result.

## Validation

The contract checks:
- empty claims
- empty URLs
- invalid URL schemes
- duplicate claims
- repeated evaluation
- invalid verdict values

## Tests

Run:

    gltest tests/test_evidencegate.py -v --network studionet

Current result:

    8 passed

## Example

Claim:

    GenLayer Studio allows developers to build Intelligent Contracts

Evidence:

    https://docs.genlayer.com

Result:

    SUPPORTED

## Current limitation

Right now one claim uses one evidence URL, and the page content is not permanently snapshotted before evaluation.

## License

MIT
