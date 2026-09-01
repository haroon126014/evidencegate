# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


class EvidenceGate(gl.Contract):
    claim: str
    evidence_url: str
    verdict: str
    reasoning: str
    evaluated: bool

    def __init__(self):
        self.claim = ""
        self.evidence_url = ""
        self.verdict = "NOT_EVALUATED"
        self.reasoning = ""
        self.evaluated = False

    @gl.public.write
    def create_claim(self, claim: str, evidence_url: str) -> None:
        claim = claim.strip()
        evidence_url = evidence_url.strip()

        if self.claim != "":
            raise gl.vm.UserError("Claim already created")

        if claim == "":
            raise gl.vm.UserError("Claim cannot be empty")

        if evidence_url == "":
            raise gl.vm.UserError("Evidence URL cannot be empty")

        if not (
            evidence_url.startswith("https://")
            or evidence_url.startswith("http://")
        ):
            raise gl.vm.UserError("Evidence URL must use HTTP or HTTPS")

        self.claim = claim
        self.evidence_url = evidence_url

    @gl.public.write
    def evaluate(self) -> None:
        if self.claim == "":
            raise gl.vm.UserError("No claim exists")

        if self.evaluated:
            raise gl.vm.UserError("Claim already evaluated")

        claim = self.claim
        evidence_url = self.evidence_url

        def evaluate_evidence():
            try:
                page = gl.nondet.web.render(
                    evidence_url,
                    mode="text"
                )
            except Exception:
                return json.dumps(
                    {
                        "verdict": "SOURCE_UNAVAILABLE",
                        "reasoning": "Evidence source could not be accessed or rendered.",
                    },
                    sort_keys=True,
                )

            prompt = f"""
Evaluate the factual claim using ONLY the supplied evidence.

CLAIM:
{claim}

EVIDENCE:
{page}

Return exactly one verdict:

SUPPORTED
CONTRADICTED
INSUFFICIENT
SOURCE_UNAVAILABLE

Definitions:

SUPPORTED:
The supplied evidence clearly establishes the claim.

CONTRADICTED:
The supplied evidence clearly conflicts with the claim.

INSUFFICIENT:
The evidence is readable but does not contain enough information
to establish or reject the claim.

SOURCE_UNAVAILABLE:
The evidence cannot meaningfully be read.

Rules:
- Do not use outside knowledge.
- Do not invent missing facts.
- Base the verdict only on the supplied evidence.
- Keep reasoning concise and factual.

Return JSON with exactly these fields:

{{
  "verdict": "SUPPORTED|CONTRADICTED|INSUFFICIENT|SOURCE_UNAVAILABLE",
  "reasoning": "brief factual explanation"
}}
"""

            result = gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

            if not isinstance(result, dict):
                raise gl.vm.UserError("LLM returned invalid output")

            verdict = str(result.get("verdict", "")).strip()

            allowed = (
                "SUPPORTED",
                "CONTRADICTED",
                "INSUFFICIENT",
                "SOURCE_UNAVAILABLE",
            )

            if verdict not in allowed:
                raise gl.vm.UserError("LLM returned invalid verdict")

            reasoning = str(result.get("reasoning", "")).strip()

            if reasoning == "":
                raise gl.vm.UserError("LLM returned empty reasoning")

            if len(reasoning) > 1000:
                reasoning = reasoning[:1000]

            return json.dumps(
                {
                    "verdict": verdict,
                    "reasoning": reasoning,
                },
                sort_keys=True,
            )

        result_json = gl.eq_principle.prompt_comparative(
            evaluate_evidence,
            principle="""
The verdict field MUST be exactly identical.

The reasoning may use different wording, but it must describe
substantially the same factual basis and must not contradict
the verdict.

Outputs with different verdicts are NOT equivalent.
""",
        )

        result = json.loads(result_json)

        self.verdict = result["verdict"]
        self.reasoning = result["reasoning"]
        self.evaluated = True

    @gl.public.view
    def get_claim(self) -> str:
        return self.claim

    @gl.public.view
    def get_evidence_url(self) -> str:
        return self.evidence_url

    @gl.public.view
    def get_verdict(self) -> str:
        return self.verdict

    @gl.public.view
    def get_reasoning(self) -> str:
        return self.reasoning

    @gl.public.view
    def is_evaluated(self) -> bool:
        return self.evaluated
