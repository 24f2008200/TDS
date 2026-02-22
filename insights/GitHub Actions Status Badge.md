## GitHub Actions Status Badge

A status badge is a small dynamic image that displays the current state of a workflow — passing, failing, or in progress — typically embedded in your README so anyone visiting the repo can instantly see the CI health.

GitHub auto-generates a badge URL for every workflow. The format is:

```
https://github.com/USER/REPO/actions/workflows/WORKFLOW_FILE.yml/badge.svg
```

To add it to your README as a clickable link:

```markdown
[![Daily Commit](https://github.com/USER/REPO/actions/workflows/daily-commit.yml/badge.svg)](https://github.com/USER/REPO/actions/workflows/daily-commit.yml)
```

The first part `[![alt text](image_url)]` is the image, and wrapping it in `(url)` makes it clickable and takes you to the workflow's run history.

---

## Manually Triggering a Workflow

Three ways to do this:

**Via the GitHub UI** — go to your repo → Actions tab → click the workflow name in the left sidebar → click the "Run workflow" dropdown on the right → select the branch → click the green "Run workflow" button.

**Via GitHub CLI:**
```bash
gh workflow run daily-commit.yml
# or target a specific branch
gh workflow run daily-commit.yml --ref main
```

**Via the REST API:**
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/USER/REPO/actions/workflows/daily-commit.yml/dispatches \
  -d '{"ref":"main"}'
```

---

## What `workflow_dispatch` Means

`workflow_dispatch` is a trigger type that exposes a manual "Run workflow" button in the GitHub Actions UI. Without it, a schedule-only workflow has no way to be triggered on demand.

```yaml
on:
  schedule:
    - cron: '30 2 * * *'
  workflow_dispatch:        # this unlocks the manual trigger button
```

You should include it for several practical reasons. First, scheduled workflows can't be tested without waiting for the cron time — sometimes hours away. Second, during initial setup you need to verify the workflow actually works before trusting it to run unattended. Third, it's useful for re-running after a failure without waiting a full day. Fourth, GitHub disables scheduled workflows on inactive repos (60-day rule), and `workflow_dispatch` lets you re-enable and re-run immediately.

You can also define input parameters with `workflow_dispatch` if you want to pass values at trigger time, though for a simple daily commit workflow you don't need that.

---

## "No Status" Badge — What's Wrong

A badge shows "no status" when GitHub can't find a completed run for that workflow on the specified branch. Common causes:

**The workflow has never run.** A schedule-only workflow won't run until its cron time fires. Add `workflow_dispatch` and trigger it manually once — the badge will update after that first run completes.

**Wrong workflow filename in the badge URL.** The filename in the URL must exactly match your `.yml` file. If your file is `daily-commit.yml` but your badge references `daily_commit.yml`, you'll get no status. Check capitalization and hyphens vs underscores.

**Wrong branch.** The badge defaults to your default branch (usually `main`). If your workflow only ran on a different branch, the badge won't reflect it. You can explicitly specify a branch:

```
https://github.com/USER/REPO/actions/workflows/daily-commit.yml/badge.svg?branch=main
```

**The workflow file has a syntax error** and was never valid enough to run. Check the Actions tab for a red error indicator.

---

## Customizing Badge Appearance

GitHub's native badge has limited customization, but you can control the branch it reflects:

```
badge.svg?branch=develop      # show status for a specific branch
badge.svg?event=push          # show status for push-triggered runs only
badge.svg?event=schedule      # show status only for scheduled runs
```

For full visual customization — different colors, styles, logos — use **Shields.io**, which wraps GitHub's workflow status in a highly configurable format:

```
https://img.shields.io/github/actions/workflow/status/USER/REPO/daily-commit.yml
```

Shields.io supports style parameters:

```
?style=flat           # default flat look
?style=flat-square    # no rounded corners
?style=for-the-badge  # large blocky badge, popular in READMEs
?style=plastic        # gradient sheen
?logo=github          # add a GitHub logo icon
&label=daily+commit   # custom label text
&color=brightgreen    # override the color regardless of status
```

A fully customized Shields.io badge in your README might look like:

```markdown
[![Daily Commit](https://img.shields.io/github/actions/workflow/status/USER/REPO/daily-commit.yml?style=for-the-badge&logo=github&label=Daily%20Commit)](https://github.com/USER/REPO/actions/workflows/daily-commit.yml)
```

For most practical purposes the native GitHub badge is sufficient — it updates in real time and requires no third-party dependency.


Let's get this done! I'll create both the workflow file and an updated README with the status badge.

I just need one thing from you first — what's your GitHub username and repository name?While you answer, let me prepare both files using your known details (`24f2008200` / `TDS-GA3-Q4`) and the daily-commit workflow we already set up:---

Here's exactly what to do to complete the assignment:

**1. Add/replace your `README.md`** with the file above — it already contains the correctly formatted badge pointing to your workflow.

**2. Make sure your `daily-commit.yml`** (also attached, with the `permissions: contents: write` fix) is in `.github/workflows/`.

**3. Trigger the workflow manually** so the badge shows green:
> Actions → Daily Automated Commit → Run workflow → Run workflow

**4. Submit** `https://github.com/24f2008200/TDS-GA3-Q4`

The critical line in your README that satisfies the requirement is:
```markdown
![Daily Commit](https://github.com/24f2008200/TDS-GA3-Q4/actions/workflows/daily-commit.yml/badge.svg)
```

Once the workflow has at least one successful run, the badge will display as **passing** (green). If it still shows "no status" after running, double-check that the `.yml` filename in the badge URL exactly matches your file in `.github/workflows/`.

Perfect — the README.md I already created is exactly right for you then! It's a fresh README tracking the `daily-commit.yml` workflow we built earlier.

**Just do these three things:**

**1. Add both files to your repo** (both are attached above):
- `README.md` → goes in the **root** of your repo
- `daily-commit.yml` → goes in `.github/workflows/`

**2. Trigger the workflow manually** to get a green badge:
> **Actions → Daily Automated Commit → Run workflow → Run workflow**

**3. Submit** `https://github.com/24f2008200/TDS-GA3-Q4`

That's it — once the workflow completes successfully, your badge will show green and the assignment requirement is fully satisfied.
