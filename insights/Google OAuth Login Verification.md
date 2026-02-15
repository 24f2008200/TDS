# eShopCo Staff Portal — Google SSO with FastAPI

A minimal but production-aware FastAPI application demonstrating Google
OpenID Connect (OAuth2) authentication for eShopCo's internal staff portal.

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Google OAuth Credentials
1. Go to https://console.cloud.google.com
2. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
3. Application type: **Web application**
4. Authorized redirect URIs: `http://localhost:8000/auth/callback`
5. Copy the Client ID and Client Secret

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and fill in GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SESSION_SECRET
```

### 4. Run
```bash
python main.py
# or
uvicorn main:app --reload
```

### 5. Visit http://localhost:8000

---

## How the OAuth2/OIDC Flow Works

```
Browser          FastAPI App         Google Auth Server
   |                  |                      |
   |-- GET /login --->|                      |
   |                  |-- redirect w/state ->|
   |<-- 302 redirect--|                      |
   |                                         |
   |-------- GET accounts.google.com ------->|
   |<------- Login + Consent UI -------------|
   |                                         |
   |-- GET /auth/callback?code=X&state=Y --->|
   |                  |                      |
   |                  |-- POST /token ------->|
   |                  |<-- {access_token,     |
   |                  |     id_token,         |
   |                  |     refresh_token} ---|
   |                  |                      |
   |                  | [validate id_token]  |
   |                  | [store in session]   |
   |<-- 302 / --------|                      |
```

---

## Key Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Home page (login button or staff portal) |
| `GET /login` | Redirects to Google consent screen |
| `GET /auth/callback` | OAuth callback — exchanges code for tokens |
| `GET /id_token` | Returns raw `id_token` as JSON (requires login) |
| `GET /logout` | Clears session |
| `GET /dashboard` | Protected: Sales dashboard |
| `GET /inventory` | Protected: Inventory management |
| `GET /support` | Protected: Support tickets |

---

## Security Checklist

- [x] **State parameter** — Authlib auto-generates and validates (CSRF protection)
- [x] **id_token signature** — Validated against Google's JWKS endpoint
- [x] **Claims checked** — `aud`, `iss`, `exp` verified by Authlib
- [x] **Session signed** — `SessionMiddleware` uses HMAC-signed cookies
- [x] **Domain restriction** — Uncomment `hd` check to lock to Workspace domain
- [ ] **HTTPS in production** — Set `https_only=True` in SessionMiddleware
- [ ] **refresh_token** — Stored server-side (DB), never in cookie
- [ ] **Token rotation** — Implement access_token refresh before expiry

---

## Token Refresh Flow (Production Pattern)

```python
import time

async def get_valid_access_token(user_id: str, db) -> str:
    token_data = await db.get_token(user_id)

    if token_data["expires_at"] - time.time() < 60:   # < 60s remaining
        new_token = await oauth.google.fetch_access_token(
            grant_type="refresh_token",
            refresh_token=token_data["refresh_token"],
        )
        await db.update_token(user_id, new_token)
        return new_token["access_token"]

    return token_data["access_token"]
```

---

## id_token Structure

The `id_token` is a **JWT** (JSON Web Token). Decode it at https://jwt.io

Example payload claims:
```json
{
  "iss": "https://accounts.google.com",
  "aud": "your-client-id.apps.googleusercontent.com",
  "sub": "1234567890",           ← Google's unique user ID
  "email": "staff@eshopco.com",
  "email_verified": true,
  "name": "Jane Doe",
  "hd": "eshopco.com",           ← Hosted domain (Workspace accounts only)
  "exp": 1700000000,             ← Expiry (Unix timestamp)
  "iat": 1699996400
}
```
