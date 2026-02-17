## What is Cloudflare Workers?

Cloudflare Workers is an edge computing platform that runs your code in 300+ data centers worldwide, executing at the location closest to each user. Unlike traditional serverless (which runs in one or a few regions), Workers run **everywhere simultaneously** with no cold starts.

**Popular alternatives:**

| Platform | Best for |
|---|---|
| **Vercel Edge Functions** | Next.js apps, frontend-adjacent logic |
| **AWS Lambda@Edge** | CloudFront CDN integration, AWS ecosystem |
| **Deno Deploy** | TypeScript-first, Deno runtime |
| **Fastly Compute** | High-performance edge, Rust/WASM |
| **Netlify Edge Functions** | JAMstack, Deno-based |
| **AWS Lambda** | Standard serverless, longer tasks, Python/Java |

**Decision tree:**
```
Do you need ultra-low global latency (edge)?
├── Yes → Cloudflare Workers (best DX + free tier)
│         Unless you're deep in AWS → Lambda@Edge
└── No → Is it frontend/Next.js?
         ├── Yes → Vercel
         └── No → Need persistent server / long tasks?
                  ├── Yes → Render, Railway, Fly.io
                  └── No → Vercel or Netlify serverless
```

---

## How Cloudflare Workers works & gotchas

**How it works:** Your code runs in the V8 engine (same as Chrome/Node) inside Cloudflare's network. Every request is handled at the nearest data center. There's no server to manage, no region to pick, and no cold starts because Workers stay warm globally.

**Limitations to know:**

- **JavaScript/TypeScript or WASM only** — no native Python, Ruby, Go etc. (more on this below)
- **CPU time limit: 10ms** on free tier, 30ms on paid — *wall clock* time can be longer (for I/O), but pure compute is capped hard
- **No Node.js built-ins by default** — `fs`, `crypto` etc. need polyfills or the Workers-specific API
- **50ms startup budget** — your entire script including imports must parse fast
- **Memory: 128MB per Worker**
- **No persistent filesystem** — use KV, R2, or D1 (their storage products) instead
- **Request size: 100MB max body**
- **Wrangler CLI required** — deployment is via their own toolchain, not generic CI

**What it means for you:** For lightweight data transformation endpoints like this case study, Workers are *ideal* — fast, free, globally distributed, zero config infrastructure.

---

## Common issues & monitoring

**Most common issues:**
- Hitting the CPU time limit (fix: keep transforms lean, avoid heavy loops)
- CORS errors from missing headers on OPTIONS preflight (fix: always handle OPTIONS explicitly)
- Forgetting `Content-Type: application/json` on responses (fix: always set it)
- `wrangler` auth issues (fix: `wrangler login` again, check `CLOUDFLARE_API_TOKEN`)
- Workers failing silently — errors return a generic Cloudflare 1101 page

**How to monitor/troubleshoot:**
- **Cloudflare Dashboard → Workers → your worker → Logs** — real-time tail logs
- **`wrangler tail`** in terminal — live log stream while testing
- **`wrangler dev`** — local development server before deploying
- **Workers Analytics** — request count, error rate, CPU time per worker

---

## Workers vs. Cloud Server — when to use which

Use **Cloudflare Workers** when you need stateless request/response logic at global low latency with zero ops overhead. Use a **cloud server** (EC2, GCE, Droplet) when you need persistent processes, heavy computation, a database co-located with compute, long-running tasks, or runtimes Workers don't support.

---

## Can you run Python FastAPI on Cloudflare Workers?

**Not directly.** Workers run the V8 JavaScript engine — there's no Python interpreter. You have two partial workarounds: compile Python to WASM (experimental, limited library support, hits CPU limits fast) or rewrite the logic in JavaScript. For a real FastAPI app, deploy to Render, Railway, or Fly.io instead. For simple endpoints like this one, just rewrite the logic in JS — it's usually 20 lines.

---

Now let's build and deploy the Worker:Now let me verify the logic locally with the exact grading payload:Logic confirmed. Now copy to outputs:Grading payload check ✅
```
Input:    "djdwwbsb vgwqa cqdxhp mdecvbo xlkphv"
Reversed: "xlkphv mdecvbo cqdxhp vgwqa djdwwbsb"
```

---

## Deploy steps (in your terminal)

**1. Install Wrangler** (Cloudflare's CLI):
```bash
npm i -g wrangler
```

**2. Login to Cloudflare:**
```bash
wrangler login
```
(Opens browser, same flow as Vercel did)

**3. Go into the folder and deploy:**
```bash
cd cf-worker
wrangler deploy
```

It will print your live URL like:
```
https://data-transform.<your-subdomain>.workers.dev
```

**Your answer for the assignment is:**
```
https://data-transform.<your-subdomain>.workers.dev/data
```

Paste the URL here once it's deployed and I'll confirm it's correct!

