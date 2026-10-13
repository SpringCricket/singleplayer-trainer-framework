# Security Policy

## Scope

`singleplayer-trainer-framework` reads and writes process memory of **single-player games running locally on your own machine**. It does not phone home, does not include a network layer, and does not touch any remote service.

## Out of scope (not accepted as vulnerabilities)

- Detection by multiplayer anti-cheat. This framework is not designed for multiplayer and will be flagged if used there. That is not a bug.
- The framework requiring elevated privileges to open a target process handle.
- Local game save corruption caused by writing bad offsets — that is a pointer-map accuracy issue, not a security issue.

## Reporting a vulnerability

Email `security@spudworks.dev` with:
- Affected version (`sptf --version`)
- Reproducer (pointer map + handler + game build)
- Impact assessment

We aim to acknowledge within 72 hours. Coordinated disclosure window: 90 days.

## Supply chain

Dependencies are pinned in `pyproject.toml`. `pymem` and `pywin32` are the only native-touching packages. If you find a malicious release published under our name, report it immediately.