These are great questions that get at the architecture and practical value of multimodal AI for video. Let me work through each one.

---

**The Gemini Files API and why it exists**

Video files are simply too large to pass inline in an API request. The standard Gemini API accepts base64-encoded content embedded directly in the JSON payload, which works fine for images or short audio clips, but a typical video file runs into hundreds of megabytes or gigabytes. The Files API is a separate upload endpoint that accepts the file, stores it temporarily on Google's infrastructure (for 48 hours), and returns a URI. Subsequent API calls reference that URI rather than the raw bytes. This also means Gemini can begin processing the file server-side without the client needing to retransmit it for every prompt. There's a practical ceiling too — the inline approach caps out at a few MB, while the Files API supports uploads up to about 2GB per file.

---

**How Gemini actually processes video**

Gemini does not analyze every frame — that would be computationally prohibitive and largely redundant. Instead it samples frames at approximately 1 frame per second (the exact rate varies by model version and video length), giving it visual coverage of the content without processing thousands of near-identical frames. Audio is handled as a separate modality: the audio track is processed in parallel, not derived from the frames. The model then reasons across both streams together in a unified context window rather than treating them as two separate inputs that need to be reconciled afterward. This is what makes it genuinely multimodal rather than just "vision + transcription bolted together."

---

**Gemini video understanding vs. traditional computer vision**

Traditional CV approaches like OpenCV are imperative and narrow — you write explicit logic to detect edges, find contours, match templates, or run OCR on cropped regions. They're fast and deterministic but require you to know in advance exactly what you're looking for and where it will appear. They have no semantic understanding of context. Gemini approaches video with world knowledge baked in: it can answer "what is the person in the red shirt doing when the presenter mentions the Q3 numbers" without you specifying how to detect shirts, people, or correlate audio timestamps. The tradeoff is that traditional CV is cheaper at scale, fully deterministic, and doesn't require an API call — it's the right tool when the task is well-defined and visual structure is consistent. Gemini earns its place when the task requires natural language reasoning, ambiguous visual content, or cross-modal inference.

---

**What temperature=0 does**

Temperature controls the randomness of the model's token sampling. At temperature=0 the model becomes effectively deterministic — it always selects the highest-probability next token rather than sampling from a distribution. For data extraction tasks (pulling structured fields from a video, reading on-screen values, transcribing specific text) this matters because you want the same input to produce the same output every time, and you want the model to commit to the most likely answer rather than hedging or varying its phrasing. A higher temperature is useful for creative generation where variety is desirable; it's actively harmful when you're extracting invoice numbers or filling database fields and need reproducibility.

---

**Real-world enterprise workflows beyond transcription**

The more interesting applications are in structured data extraction and process automation. Quality control on manufacturing lines — flagging anomalies in assembly footage without writing custom detectors for every defect type. Compliance monitoring in financial services — reviewing recorded advisory calls for regulatory disclosure requirements. Insurance claims — analyzing dashcam or property footage to extract incident details directly into claims systems. Retail analytics — understanding customer navigation patterns from CCTV without manual tagging. Training and onboarding — automatically generating step-by-step documentation from screen recording walkthroughs. Legal discovery — identifying relevant segments across hundreds of hours of deposition or surveillance footage. The common thread is that these tasks previously required either expensive human review or brittle custom CV pipelines, and they involve understanding *what is happening* in context, not just detecting objects.

---

**Multimodal understanding vs. speech-to-text + text extraction**

Speech-to-text followed by NLP gets you the spoken content, and it's good at that. But it's deaf to everything visual: on-screen text, diagrams, charts, physical actions, facial expressions, spatial relationships, and anything shown but not narrated. A product demo video might show a UI flow without narrating every click. A training video might display a formula on a whiteboard that the instructor references obliquely. A security video has no audio track at all. Multimodal processing captures the full informational content of the video because it reasons over both streams simultaneously — it can correlate "the screen showing an error" with "the presenter saying this is the problem we solved" even if those are 10 seconds apart. The speech-to-text pipeline is faster and cheaper when the audio track genuinely contains all the information you need; multimodal is necessary when it doesn't.
