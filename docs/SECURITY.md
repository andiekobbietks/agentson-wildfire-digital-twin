# Security, safety and responsible use

## Scope

This repository describes a simulation and research demonstrator. It is not an operational wildfire command platform. The project must not be used to direct real aircraft, dispatch responders, issue public warnings, or make life-safety decisions.

## Data handling

- Use public or explicitly authorised datasets.
- Review dataset and asset licences before downloading, storing, or redistributing.
- Do not commit credentials, API tokens, private keys, personal data, or restricted operational information.
- Keep large datasets and generated sensor recordings out of Git unless there is a clear licence and repository-size justification.
- Store source identifiers, retrieval dates, checksums, and transformations in manifests.
- Clearly label synthetic and generated data.

## Software supply chain

- Pin dependency versions for reproducible runs.
- Record simulator, middleware, autopilot, model, and runtime versions.
- Review upstream advisories and dependency licences.
- Prefer signed releases and checksums where available.
- Do not run untrusted models, plugins, or scripts on privileged hosts.
- Use least-privilege credentials for any external data access.

## AgentSON trace integrity

AgentSON records should preserve event identity, sequence, provenance, and integrity metadata. Integrity checks can indicate whether a recorded trace has changed since it was created. They do not establish that sensor observations were accurate, a dataset was authoritative, or an agent decision was correct. Preserve the distinction between provenance, integrity, authenticity, and truth.

## Simulation and autonomy boundary

- Keep all vehicle activity in simulation for the MVP.
- Make simulation state unmistakable in logs and user interfaces.
- Do not connect to real flight controllers or aircraft.
- Do not present a perception result as a confirmed fire or emergency.
- Do not infer operational readiness from SITL success.
- Any later field test requires separate legal, regulatory, organisational, and safety review.

## Incident handling

If a credential or sensitive artefact is accidentally committed:
1. Revoke or rotate the exposed credential immediately.
2. Remove it from the current repository state.
3. Assess whether history rewriting and downstream notification are required.
4. Review access logs where available.
5. Document the incident and corrective actions without reproducing the secret.

Report suspected vulnerabilities privately to the repository maintainer rather than publishing exploit details in an issue.
