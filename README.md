# Dependabot Demo

A Python project demonstrating automated dependency security updates with GitHub Dependabot.

## About

This repository is configured with Dependabot to automatically monitor Python dependencies in `requirements.txt` and open pull requests within 24 hours of any CVE disclosure.

## Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | Web framework for building APIs |
| `requests` | HTTP library |
| `pandas` | Data analysis and manipulation |
| `uvicorn` | ASGI server for FastAPI |

## Dependabot Configuration

Dependabot is configured to:
- Check `pip` dependencies **weekly**
- Prefix all dependency update commits with `deps:`
- Automatically open PRs when vulnerabilities or newer versions are found

## Case Study

A production API was using a vulnerable version of the `requests` library for 6 months. With Dependabot configured, teams now get automatic PRs within 24 hours of any CVE disclosure, keeping dependencies secure without manual monitoring.

## Contact

24f2008200@ds.study.iitm.ac.in
