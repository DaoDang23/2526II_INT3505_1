import json
import requests

BASE = "http://localhost:5005"
ACTION_URL = f"{BASE}/action"
TOKEN = "secret-token-alice"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Local ETag cache: url → etag value
etag_store: dict[str, str] = {}

# ── Display helper ────────────────────────────────────────────────────────────

def show(label: str, response: requests.Response) -> None:
    sep = "=" * 56
    print(f"\n{sep}")
    print(f"  {label}")
    print(f"  {response.request.method} {response.request.url}")
    print(f"  Status : {response.status_code}")

    # Print selected request/response headers when present
    interesting_headers = {
        "Authorization": "Auth   ",
        "ETag":          "ETag   ",
        "Cache-Control": "Cache  ",
        "Location":      "Loc    ",
    }
    req_auth = response.request.headers.get("Authorization")
    if req_auth:
        print(f"  Auth   : {req_auth}")

    for header, label_str in [("ETag", "ETag   "), ("Cache-Control", "Cache  "), ("Location", "Loc    ")]:
        value = response.headers.get(header)
        if value:
            print(f"  {label_str}: {value}")

    if response.status_code == 304:
        print("  → 304 Not Modified: dùng bản cache, server không gửi body")
        return

    if not response.text:
        return

    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except ValueError:
        print(response.text)

# ── RPC call ──────────────────────────────────────────────────────────────────

def call_action(action: str, **kwargs) -> requests.Response:
    payload = {"action": action, **kwargs}
    response = requests.post(ACTION_URL, json=payload, timeout=10)
    show(f"[RPC] {action}", response)
    return response

# ── REST calls ────────────────────────────────────────────────────────────────

def get_with_cache(path: str, label: str) -> requests.Response:
    """GET with conditional ETag support."""
    url = f"{BASE}{path}"
    headers = dict(HEADERS)

    cached_etag = etag_store.get(url)
    if cached_etag:
        headers["If-None-Match"] = cached_etag
        print(f"\n  [Cache] Gửi If-None-Match: {cached_etag[:12]}...")

    response = requests.get(url, headers=headers, timeout=10)
    show(label, response)

    new_etag = response.headers.get("ETag")
    if response.status_code == 200 and new_etag:
        etag_store[url] = new_etag

    return response


def rest_call(
    method: str,
    path: str,
    label: str,
    use_auth: bool = True,
    **kwargs,
) -> requests.Response:
    """Generic REST call with optional Bearer auth."""
    url = f"{BASE}{path}"
    extra_headers = kwargs.pop("headers", {})
    auth_headers = HEADERS if use_auth else {}
    merged = {**auth_headers, **extra_headers}

    response = requests.request(method, url, headers=merged, timeout=10, **kwargs)
    show(label, response)
    return response

# ── Demo script ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Demo A: Legacy RPC ────────────────────────────────────────────────────
    print("\n" + "━" * 56)
    print("  DEMO A: Legacy RPC (/action) - từ V1")

    call_action("get_users")
    call_action("get_user", id=1)
    call_action("create_user", name="Dave", email="dave@example.com")
    call_action("update_email", id=2, email="bob_legacy@example.com")
    call_action("delete_user", id=3)

    # ── Demo B: REST + Auth + ETag Cache ──────────────────────────────────────
    print("\n" + "━" * 56)
    print("  DEMO B: REST + Auth + Cache (ETag) - từ V2/V3/V4")

    get_with_cache("/users", "GET /users (lần 1)")
    get_with_cache("/users", "GET /users (lần 2, ETag match)")

    rest_call("POST", "/users", "POST create user", json={"name": "Eve", "email": "eve@example.com"})
    get_with_cache("/users", "GET /users (sau POST, ETag đổi)")

    rest_call("PUT",    "/users/2", "PUT update user id=2", json={"email": "bob_rest@example.com"})
    rest_call("DELETE", "/users/1", "DELETE user id=1")

    rest_call("GET", "/users", "GET /users (no token) → 401", use_auth=False)
    rest_call(
        "GET", "/users/2",
        "GET with INVALID token → 401",
        use_auth=False,
        headers={"Authorization": "Bearer fake-token"},
    )
    rest_call("GET", "/users/999", "GET /users/999 → 404")
