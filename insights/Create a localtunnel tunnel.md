## Q1 — What is Localtunnel & Alternatives

**Localtunnel** is a free, open-source tool that exposes your local server to the internet via a public URL — no account, no install beyond npm, no config. It works by creating a tunnel from a `loca.lt` subdomain to your `localhost`.

**Popular modern alternatives:**

| Tool | Free tier | Account needed | Custom domain | Best for |
|---|---|---|---|---|
| **ngrok** | Yes (limited) | Yes | Paid | Professional dev/testing |
| **Cloudflare Tunnel** | Yes (unlimited) | Yes | Yes (free) | Production-grade, permanent |
| **Tailscale Funnel** | Yes | Yes | No | Team/private sharing |
| **bore** | Yes | No | No | Self-hosted, minimal |
| **serveo** | Yes | No | No | SSH-only, zero install |

**Decision tree — what to use when:**

```
Do you need it permanently / in production?
├── YES → Cloudflare Tunnel (free, stable, custom domain)
└── NO → Is it just for quick local testing?
         ├── YES → Do you need zero setup / no account?
         │         ├── YES → localtunnel (npx, instant, throwaway)
         │         └── NO  → ngrok (more reliable, better dashboard)
         └── NO → Do you need private team access only?
                  └── YES → Tailscale Funnel
```

---

## Q2 — How Localtunnel Works & Gotchas

**How it works:** When you run `lt --port 8000`, localtunnel's client opens a persistent TCP connection to `localtunnel.me` servers. The server assigns you a subdomain and forwards any incoming HTTP requests through that connection to your local port. Your machine is the actual web server — localtunnel is just a relay.

```
Browser → https://xyz.loca.lt → localtunnel.me server → your machine:8000
```

**Key gotchas you must know:**

- **Password wall** — first visit shows a "Friendly Reminder" page asking visitors to confirm they understand it's a tunnel. This breaks automated testers/portals. Fix: always pass the `--header` bypass or use the tunnel's IP directly.
- **Unreliable uptime** — it's a free community service, connections drop randomly. Not for anything important.
- **No account = no persistence** — URL changes every restart unless you use `--subdomain` (not guaranteed to be available).
- **Speed** — all traffic routes through US servers, so latency can be high from India.
- **What it means for you** — for this assignment, the portal will hit your tunnel URL directly, so you need the server running and the tunnel active at submission time.

---

## Q3 — localtunnel vs ngrok vs Cloudflare Tunnel

| | localtunnel | ngrok | Cloudflare Tunnel |
|---|---|---|---|
| **Setup** | `npx localtunnel` — zero account | Account + authtoken | Account + `cloudflared` daemon |
| **Reliability** | Low (community servers) | High | Very high (Cloudflare's network) |
| **Password wall** | Yes (annoying) | No | No |
| **Custom subdomain** | Unstable | Paid | Free |
| **Speed** | Slow | Fast | Very fast |
| **Use case** | Throwaway demos | Dev/webhook testing | Permanent / production |

**Rule of thumb:** localtunnel for a 5-minute assignment demo, ngrok for daily dev work, Cloudflare for anything that needs to last.

---

## Setting Up Localtunnel for the Assignment

**Step 1 — Install and start the tunnel:**
```bash
# Install Node.js first if needed, then:
npx localtunnel --port 8000
```
It'll output something like:
```
your url is: https://thick-cats-agree.loca.lt
```

**Step 2 — Add an endpoint that serves your email:**---

## Now set up localtunnel — full steps:

**Step 1 — Restart your server** with the new file:
```bash
python upload.py
```

**Step 2 — In a new terminal, start localtunnel:**
```bash
npx localtunnel --port 8000
```
It'll print something like:
```
your url is: https://thick-cats-agree.loca.lt
```

**Step 3 — Bypass the password wall** (critical — the portal can't click through it):
```bash
npx localtunnel --port 8000 --local-host localhost
```
Then visit your tunnel URL once in a browser and click through the warning page manually. After that, automated requests will work.

**Step 4 — Verify it works:**
```bash
curl https://thick-cats-agree.loca.lt/
# Should return: {"email": "24f2008200@ds.study.iitm.ac.in"}
```

**Step 5 — Submit** the URL the portal asks for. Depending on what it wants, it could be:
- `https://thick-cats-agree.loca.lt/` — returns your email at root
- `https://thick-cats-agree.loca.lt/upload` — the upload endpoint

Try the root URL first — what does the portal's input field label say exactly?
