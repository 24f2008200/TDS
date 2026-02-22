## Cron Syntax

Cron uses five fields separated by spaces representing: **minute, hour, day-of-month, month, day-of-week**.

```
┌───── minute (0-59)
│ ┌───── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌───── month (1-12)
│ │ │ │ ┌───── day of week (0-7, where 0 and 7 = Sunday)
│ │ │ │ │
* * * * *
```

So `0 * * * *` means: **at minute 0 of every hour, every day** — i.e., once per hour on the hour. An asterisk means "every valid value" for that field. Other common patterns:

- `0 9 * * 1-5` — 9:00 AM on weekdays
- `*/15 * * * *` — every 15 minutes
- `0 0 1 * *` — midnight on the 1st of every month
- `30 6 * * 0` — 6:30 AM on Sundays

---

## Why GitHub Actions Instead of a Server Cron?

The main advantages are **no infrastructure to manage**. With a server cron you need a machine that's always on, patched, and monitored. GitHub Actions gives you:

- Zero server costs for typical scheduled tasks (within free tier minutes)
- The runner environment is ephemeral and clean every run
- Logs, history, and failure notifications are built in
- Your schedule lives in version control alongside the code it operates on
- Easy secrets management via repository secrets
- No SSH access, no server uptime concerns

The tradeoff is you're dependent on GitHub's infrastructure and have less control over the exact runtime environment.

---

## Limitations of GitHub Actions Scheduled Workflows

The big ones to know about:

**Timing is not precise.** GitHub queues scheduled workflows and runs them when runners are available. During high load periods (especially the top of the hour), your `0 * * * *` job might actually fire 15–30 minutes late. Don't use it for anything time-critical.

**Inactive repos get disabled.** If a repository has no activity for 60 days, GitHub disables scheduled workflows automatically (more on this below).

**Minimum interval is 5 minutes.** You can't schedule more frequently than `*/5 * * * *`.

**Free tier minutes are limited.** Public repos get unlimited minutes; private repos have a monthly cap (2,000 minutes on the free plan). Scheduled jobs eat into this.

**No guarantee of execution.** GitHub may skip runs during outages without retroactive makeup runs.

---

## Testing Without Waiting for the Schedule

The cleanest approach is to add `workflow_dispatch` as a trigger, which adds a manual "Run workflow" button in the Actions UI:

```yaml
on:
  schedule:
    - cron: '0 * * * *'
  workflow_dispatch:  # add this
```

You can then trigger it manually from the Actions tab, or via the GitHub CLI:

```bash
gh workflow run your-workflow.yml
```

You can also temporarily change the cron to run in a few minutes (e.g., `*/2 * * * *`), push, watch it run, then revert — but `workflow_dispatch` is cleaner and you should probably keep it permanently anyway.

---

## Inactive Repository Disabling

If your repository receives **no activity for 60 days**, GitHub automatically disables all scheduled workflows and sends you an email. "Activity" means commits, pull requests, issues, etc. — the schedule firing does *not* count as activity.

To re-enable, go to Actions → find the disabled workflow → click "Enable workflow."

To prevent this from happening, common strategies include having the scheduled workflow itself commit something (a log file, a timestamp), or using `workflow_dispatch` periodically. If you're building something like a data pipeline where the repo is genuinely dormant between updates, this is a real operational concern to plan for.

---

## Committing Changes Back to the Repo

You need to configure git identity and use the `GITHUB_TOKEN` that Actions provides automatically:

```yaml
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Make your changes
        run: |
          echo "$(date)" >> log.txt

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          git diff --staged --quiet || git commit -m "chore: automated update"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The `git diff --staged --quiet ||` part is important — it skips the commit entirely if there are no changes, preventing empty commits from cluttering your history. Note that commits made by `GITHUB_TOKEN` will **not** trigger other workflows by default (to prevent infinite loops).

---

## Cron Jobs vs. Systemd Timers

Both schedule recurring tasks on Linux, but they differ quite a bit in design philosophy.

**Cron** is the classic, universally available tool. It's simple, uses the familiar five-field syntax, and every sysadmin knows it. Each user has their own crontab (`crontab -e`), and system-wide jobs live in `/etc/cron.d/`. The main weaknesses are that output handling is awkward (it emails stdout/stderr, which nobody wants), there's no dependency management, and if the system is off when a job was supposed to run, it's simply missed.

**Systemd timers** are more powerful but more verbose. Each timer is a `.timer` unit paired with a `.service` unit. Key advantages over cron:

- `OnBootSec` and `Persistent=true` let you catch up missed runs after the system was off
- Output goes to the systemd journal, so `journalctl -u yourjob` gives you structured, searchable logs
- You can express "run 5 minutes after boot" or "run 1 hour after the last run finished" — not just wall-clock times
- Full integration with systemd dependencies, sandboxing, and resource limits
- `systemctl status mytimer` tells you the last run time, next run time, and whether it succeeded

The practical rule of thumb: if you're already using systemd (any modern Linux distro), timers are worth the extra setup for anything serious. For quick personal scripts or anything needing maximum portability, cron is fine.



