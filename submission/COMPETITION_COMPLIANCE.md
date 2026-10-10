# JunctionX competition compliance review

Reviewed on 2026-10-10 against the user-supplied
NOS - JunctionX Lisbon 2026.pdf, pages 2-5. This review covers repository
structure, local changes, submission artifacts and the documented workflow.
It is not a competition eligibility certification or a live-model evaluation.

## Explicit rules and local evidence

| Requirement | Source | Local evidence / remaining work |
|---|---|---|
| One public team fork; work outside main | p.3 | Current branch: team-portwineoverflow. Remote visibility and collaborator access still need verification. |
| Preserve history; each member commits from their account | p.3 | Recent history includes team PR merges. No commits or pushes made by this review. Verify contributor identities before delivery. |
| Work inside submission/ | p.3 | New rules, privacy code, tests and documentation remain inside submission/. |
| LLM detects sensitive data using context | p.2 | submission/agent implements a Gemini pipeline; tests can use stubs. Live quality has not been established here. |
| One asterisk per anonymized word; preserve layout except empty lines | p.2 | Three-agent text model implements a provisional word/punctuation rule. Verify final candidate against source; privacy detection alone cannot check formatting. |
| Keep supplied filenames and clean generated output | p.4 | submission.txt exists but is empty: BLOCKED for final delivery. It was not populated with fabricated content. |
| Exact prompt that generated the output | p.4 | prompt.txt exists but is empty: BLOCKED for final delivery. Save the real prompt and output together when the team selects its final run. |
| Include development code and setup/usage docs | pp.4-5 | Agent and three-agent workspace exist with READMEs. Optional privacy setup documented separately. |
| Reference open-source packages | pp.2,5 | Privacy packages and model links documented in NOS_Three_Agents/README.md; review references for the other components before delivery. |
| Open-source licence | p.5 | Root LICENSE is MIT. Preserve it. |
| Automatic evaluation and flake8 | p.5 | Three organiser workflows exist. Repository flake8 passed locally before these adjustments. Missing files can still produce skipped green checks. |
| Final PR to original repository main | p.4 | Not created by this review. Confirm target repository and include all required artifacts. |
| JunctionX registration with PR link | p.4 | External/manual step, not verified. |
| Pitch at most two minutes | p.5 | Prepare and time the team's pitch. |

## Git clarification

The PDF does not ban additional working branches; it explicitly evaluates
branches and merges. The user nevertheless requires this task to remain on
team-portwineoverflow. That preference is recorded in AGENTS.md.

The previous generic rebase recommendation is superseded for this project.
Preserve collaboration history using merge-based integration. Before pulling,
review local changes and save them without discarding work. Never squash or
force-push over the team's history.

## Review findings

- Earlier privacy additions made heavy optional libraries mandatory in the
  base requirements. They are now isolated in requirements-privacy.txt.
- Ordinary tests must not depend on an unfinished competition submission.
  Real-document checking is selected with NOS_PRIVACY_DOCUMENT; an explicit
  empty/missing document remains an error.
- A small NER model can flag harmless header names that the brief's example
  keeps, and can miss sensitive data. Findings require human review and must
  not silently rewrite the submission or determine eligibility.
- The brief does not explicitly resolve multi-prompt pipelines or deterministic
  rendering. The existing evidence table records those uncertainties.
- A combined local test run stopped at collection because langchain_core is
  missing from Python 3.12. This does not establish a defect in teammate code.
- Root tutorial text is generic and includes older event details. Use the
  supplied JunctionX brief for event-specific requirements; preserve originals.

## Final delivery gate

1. Review only the intended diff, preserve teammate changes, and run relevant
   offline tests plus repository flake8.
2. Generate a real candidate through the selected LLM pipeline; preserve the
   exact prompt and provenance. Check masking, formatting and false findings.
3. Confirm submission/submission.txt and submission/prompt.txt are nonempty,
   contain the required content, and accompany the development code.
4. Confirm public fork, licence, setup instructions and library references.
5. Commit with the actual contributor identity and preserve merge history.
6. After team approval, push, open the PR to the original repository main,
   inspect actual evaluation results, and register the PR link on JunctionX.
7. Prepare a pitch within two minutes.
