# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please open an issue or contact the maintainer directly.

Since this tool only reads data from public APIs and does not handle sensitive user data, the attack surface is limited. However, we take all reports seriously.

## Security Considerations

- This tool makes requests to external APIs (Sleeper, FantasyCalc)
- Cached data is stored locally in `~/.cache/sleeper-gini/`
- No authentication tokens or sensitive data are stored
