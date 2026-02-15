Let me read the skill file first, then build this properly.No CSV file uploaded yet — that's fine, I'll build the full solution now. Let me answer all three questions first, then build the app.

---

## Q1 — How to upload files in FastAPI

FastAPI handles file uploads via `multipart/form-data` using `UploadFile`:

```python
from fastapi import FastAPI, UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```
The field name in the form (`file` here) must match what the client sends.

---

## Q2 — File Validation (and why extension checks aren't enough)

Checking only the extension is **not secure** — anyone can rename `malware.exe` to `malware.csv`. Proper validation has three layers:

- **Extension check** — first basic filter (`.csv`, `.json`, `.txt`)
- **MIME type check** — read the actual `content_type` from the upload header
- **Magic bytes check** — read the first few bytes of the file itself (most reliable). A real CSV starts with printable ASCII; a real PNG starts with `\x89PNG` regardless of its name.

For this assignment the extension + size check is what's specified, but in production you'd do all three.

---

## Q3 — HTTP Error Codes and Why They Matter Practically

| Situation | Code | Why it matters |
|---|---|---|
| Wrong/missing token | `401 Unauthorized` | Client knows to re-authenticate |
| Wrong file type | `400 Bad Request` | Client knows the request itself is malformed |
| File too large | `413 Payload Too Large` | Client knows to compress/split the file |

Practically, correct codes let clients (and monitoring tools) handle errors automatically — a `401` triggers a re-login flow, a `413` triggers a retry with a smaller chunk. Using `400` for everything breaks this.

---

## Full Implementation---

## How to Run & Test

**Install and start:**
```bash
pip install -r requirements.txt
python upload.py
```

**Test with curl** (once you have the CSV file downloaded):
```bash
curl -X POST http://localhost:8000/upload \
  -H "X-Upload-Token-1884: 24cpky1c7frqekp4" \
  -F "file=@data.csv"
```

**Expected response:**
```json
{
  "email": "24f2008200@ds.study.iitm.ac.in",
  "filename": "data.csv",
  "rows": 27,
  "columns": ["id", "name", "value", "category"],
  "totalValue": 14295.04,
  "categoryCounts": {"B": 10, "C": 4, "A": 10, "D": 3}
}
```

**Test the error cases too:**
```bash
# 401 — wrong token
curl -X POST http://localhost:8000/upload -H "X-Upload-Token-1884: wrongtoken" -F "file=@data.csv"

# 400 — wrong file type
curl -X POST http://localhost:8000/upload -H "X-Upload-Token-1884: 24cpky1c7frqekp4" -F "file=@image.png"

# 413 — file too large (make a big file to test)
```

Once it's running, submit your `http://localhost:8000/upload` as the endpoint URL to the portal. Download the test CSV from the assignment page, upload it, and the portal will verify the response matches exactly.
