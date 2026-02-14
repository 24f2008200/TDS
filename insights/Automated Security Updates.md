Let me cover the concepts thoroughly, then give you all the files you need.

---

## What is Dependabot?

Dependabot is GitHub's **built-in dependency update bot**. It watches your dependency files (`requirements.txt`, `package.json`, `Gemfile`, etc.), and when a newer version or a security vulnerability (CVE) is found, it automatically opens a Pull Request with the fix. It has two modes: **Dependabot Alerts** (just warns you) and **Dependabot Security Updates** (opens PRs automatically).

---

## Popular Modern Alternatives

| Tool | Best for | Key differentiator |
|---|---|---|
| **Renovate** (Mend) | Teams wanting deep control | Highly configurable, groups PRs, self-hostable |
| **Snyk** | Security-first teams | CVE database + code scanning + licensing checks |
| **Socket.dev** | Supply chain attacks | Detects malicious packages, not just vulnerable ones |
| **FOSSA** | Enterprise / legal compliance | License compliance focus |
| **Whitesource (Mend)** | Large enterprises | SBOM generation, policy enforcement |

---

## Decision Tree: What to Use When

```
Do you use GitHub?
├── No → Renovate (self-hosted) or Snyk
└── Yes
    ├── Small team / simple project?
    │   └── ✅ Dependabot — zero config, built-in, free
    ├── Need PR grouping, monorepos, fine-grained scheduling?
    │   └── ✅ Renovate — far more configurable than Dependabot
    ├── Security + compliance is the primary concern?
    │   └── ✅ Snyk or Socket.dev
    ├── Supply chain / malicious package risk?
    │   └── ✅ Socket.dev (unique capability)
    └── Enterprise with license/legal requirements?
        └── ✅ FOSSA or Mend (Whitesource)
```

---

## When is it OK to Ignore Dependabot Alerts?

**Legitimately OK to ignore:**
- The vulnerable code path is **not reachable** in your app (e.g., a server-side vuln in a CLI-only tool)
- The dependency is **dev/test only** and never runs in production
- A **fix doesn't exist yet** and you've documented a mitigation
- The CVE severity is **Low** and the cost of upgrading breaks more than it protects

**When people ignore alerts and shouldn't:**
- "We'll do it next sprint" — sprints pass, 6 months later the vuln is exploited (exactly the case study above)
- "It's just a minor version" — breaking CVEs exist in minor versions too
- PR merge fatigue — too many Dependabot PRs → developers start dismissing without reading
- "Our firewall protects us" — defense in depth still requires patching
- Transitive dependency alerts — "we didn't write that code" doesn't reduce your exposure

---

## Most Popular Dependabot Customizations

**1. Grouping PRs** — instead of 10 PRs, get 1:
```yaml
groups:
  production-deps:
    patterns: ["fastapi*", "requests*"]
```

**2. Limiting open PRs** — prevents PR flood:
```yaml
open-pull-requests-limit: 5
```

**3. Auto-assign reviewers:**
```yaml
reviewers:
  - "your-username"
```

**4. Targeting a specific branch** other than main:
```yaml
target-branch: "develop"
```

**5. Ignoring specific packages or versions:**
```yaml
ignore:
  - dependency-name: "pandas"
    versions: ["2.x"]
```

---

Now let me create all the files for the assignment:All three files are ready. Here's your exact repo structure to push:

```
your-repo/
├── .github/
│   └── dependabot.yml     ← exact config from the assignment
├── requirements.txt        ← fastapi, requests, pandas, uvicorn (pinned old versions)
└── README.md               ← contains 24f2008200@ds.study.iitm.ac.in
```

### Steps to push

```bash
git init
git add .
git commit -m "Add Dependabot config and Python dependencies"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Why pinned old versions matter

The `requirements.txt` uses **intentionally older pinned versions** (`fastapi==0.100.0`, `requests==2.28.0`, etc.). This means Dependabot will almost certainly find real updates to propose — and possibly real CVEs — making the demo realistic and verifiable by the grader.

### What the grader will check

1. `.github/dependabot.yml` exists with the exact config (`pip`, weekly, `deps` prefix)
2. `requirements.txt` has ≥ 3 dependencies
3. `README.md` contains `24f2008200@ds.study.iitm.ac.in`
4. Repo is **public**

Your repo URL to submit: `https://github.com/YOUR_USERNAME/YOUR_REPO`
