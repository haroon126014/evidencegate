# EvidenceGate

EvidenceGate is a GenLayer Intelligent Contract that verifies factual claims against public evidence using validator consensus.

A user submits:
- a factual claim
- a public evidence URL

Validators classify the claim as:
- `SUPPORTED`
- `CONTRADICTED`
- `INSUFFICIENT`
- `SOURCE_UNAVAILABLE`

The final verdict and reasoning are stored on-chain.

## How it works

1. Call `create_claim(claim, evidence_url)`
2. Call `evaluate()`
3. Validators independently inspect the evidence
4. GenLayer consensus determines the result
5. Verdict and reasoning are stored

## Verdicts

`SUPPORTED` — evidence clearly supports the claim.

`CONTRADICTED` — evidence clearly conflicts with the claim.

`INSUFFICIENT` — evidence is readable but not enough to decide.

`SOURCE_UNAVAILABLE` - evidence cannot meaningfully be accessed.

## Public methods

Write:
- `create_claim(claim, evidence_url)`
- `evaluate()`

View:
- `get_claim()`
- `get_evidence_url()`
- `get_verdict()`
- `get_reasoning()`
- `is_evaluated()`

## Consensus

EvidenceGate uses:
- `gl.nondet.web.render`
- `gl.nondet.exec_prompt`
- `gl.eq_principle.prompt_comparative`

The verdict must match exactly between equivalent validator outputs.

## Validation

The contract:
- rejects empty claims
- rejects empty evidence URLs
- accepts only HTTP/HTTPS URLs
- prevents duplicate claims
- prevents repeated evaluation
- restricts verdicts to four allowed values

## Tests

StudioNet integration tests:

    gltest tests/test_evidencegate.py -v --network studionet

Current result:

    8 passed

## Example

Claim:

    GenLayer Studio allows developers to build Intelligent Contracts

Evidence:

    https://docs.genlayer.com

Observed result:

    SUPPORTED

## Limitations

EvidenceGate currently:

- evaluates one evidence URL per claim
- does not cryptographically snapshot webpage content
- does not support claim updates
- does not assign confidence scores
- is intended for factual rather than subjective claims

## License

MIT
