
## Why does AIpipe exist?

Normally to use GPT or Gemini you need a **credit card** to get an API key, and you pay per request. Your professor has set up AIpipe so that **he pays** and gives you free access through your college Google account. You just log in with Google and get a token — no payment, no API key setup.

```
You  →  aipipe.org  →  OpenAI / Gemini / OpenRouter
         (professor's budget pays here)
```

---

## What can you do with it?

Based on the README, here's everything available to you:

**Chat with LLMs (text in, text out)**
Talk to GPT-4o, Gemini 2.5 Flash, Claude, Llama — any model on OpenRouter. This is what most assignments will use. You send a message, get a reply.

**Generate images**
Ask Gemini Flash Image or other image models to draw something. Useful for building creative tools or demos.

**Transcribe audio**
Send an audio file to `gpt-4o-transcribe` and get text back. Good for lecture notes, interviews, etc.

**Embeddings**
Convert text into numbers (vectors) that represent meaning. Used for semantic search, document similarity, clustering. For example — "find all student essays that are about climate change."

**Similarity API** (a bonus aipipe feature)
Send a list of documents and topics, it tells you how similar they are — without you needing to write any embedding math yourself.

**CORS Proxy** (`/proxy/URL`)
Fetch any URL from inside a browser without CORS errors. Useful when building web apps that need to read external websites.

---

## How do you actually use it? (3 ways)

**Way 1 — In a browser HTML file (simplest, no install)**
```html
<script type="module">
  import { getProfile } from "https://aipipe.org/aipipe.js";
  const { token } = getProfile();
  if (!token) window.location = `https://aipipe.org/login?redirect=${window.location.href}`;

  const res = await fetch("https://aipipe.org/openrouter/v1/chat/completions", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "openai/gpt-4o-mini",
      messages: [{ role: "user", content: "Explain photosynthesis" }]
    })
  }).then(r => r.json());

  console.log(res.choices[0].message.content);
</script>
```
Save as `index.html`, open in browser — it redirects you to Google login once, then works forever.

**Way 2 — In Python (what we were doing for your video task)**
```bash
export OPENAI_API_KEY=$AIPIPE_TOKEN
export OPENAI_BASE_URL=https://aipipe.org/openai/v1
```
Then any Python code using the `openai` library just works — it talks to aipipe instead of OpenAI directly.

**Way 3 — Command line (quick tests)**
```bash
export AIPIPE_TOKEN="your-token-from-aipipe.org"
curl https://aipipe.org/openrouter/v1/chat/completions \
  -H "Authorization: Bearer $AIPIPE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": "Hello!"}]}'
```

---

## How to get your token

1. Go to **https://aipipe.org/login**
2. Sign in with your **college Google account**
3. Copy the token shown — it looks like a long random string
4. `export AIPIPE_TOKEN=paste-it-here`

---

## For your video task specifically

Now that I know aipipe supports the **OpenAI-compatible format**, I should update your `main.py` to use that route instead of the raw Gemini format — it's cleaner and supports more models. Want me to rewrite it using `openai/gpt-4o` via aipipe (which supports vision/video) or stick with Gemini? Either works with your token.
