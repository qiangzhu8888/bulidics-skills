"""Read-only 1NCE API example; Python standard library only. No live tests bundled."""
import argparse
import base64
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler

BASE = "https://api.1nce.com/management-api"

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def request_json(method, path, authorization, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = Request(BASE + path, data=data, method=method,
                  headers={"Authorization": authorization, "Content-Type": "application/json", "Accept": "application/json"})
    try:
        with build_opener(NoRedirect()).open(req, timeout=20) as response:
            raw = response.read(4 * 1024 * 1024 + 1)
            if len(raw) > 4 * 1024 * 1024:
                raise RuntimeError("Response exceeds example client limit; reduce page size.")
            return json.loads(raw)
    except HTTPError as exc:
        # Avoid returning response bodies that could contain sensitive data.
        retry_after = exc.headers.get("Retry-After", "unspecified") if exc.code == 429 else None
        raise RuntimeError(f"HTTP {exc.code}" + (f"; Retry-After={retry_after}" if retry_after else "")) from None
    except URLError:
        raise RuntimeError("Network or TLS connection failed") from None

def get_token():
    client = os.environ.get("ONE_NCE_CLIENT_ID")
    secret = os.environ.get("ONE_NCE_CLIENT_SECRET")
    if not client or not secret:
        raise ValueError("Set ONE_NCE_CLIENT_ID and ONE_NCE_CLIENT_SECRET in the environment.")
    auth = base64.b64encode(f"{client}:{secret}".encode()).decode()
    result = request_json("POST", "/oauth/token", "Basic " + auth, {"grant_type": "client_credentials"})
    token = result.get("access_token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("Token response has no access_token")
    return token

def build_path(args):
    if not re.fullmatch(r"[0-9]{18,22}", args.iccid):
        raise ValueError("ICCID must be an 18-22 digit string; retain leading zeros.")
    if args.action == "history":
        if not args.allow_documented_os_v1:
            raise ValueError("Historian uses a documented /v1/ path: confirm current account support, then pass --allow-documented-os-v1.")
        query = {"iccid": args.iccid, "pageSize": args.page_size}
        for field, key in [("start", "startDateTime"), ("end", "endDateTime"), ("next_token", "nextToken")]:
            value = getattr(args, field)
            if value:
                query[key] = value
        return "/v1/inspect/devices/history?" + urlencode(query)
    suffix = {"sim": "", "status": "/status", "quota": "/quota/data"}[args.action]
    return "/v2/sims/" + args.iccid + suffix

def main():
    parser = argparse.ArgumentParser(description="Read one page/resource from 1NCE. Never changes SIM or webhook configuration. Output may contain device identifiers.")
    parser.add_argument("action", choices=["sim", "status", "quota", "history"])
    parser.add_argument("--iccid", required=True)
    parser.add_argument("--start", help="Historian ISO start timestamp")
    parser.add_argument("--end", help="Historian ISO end timestamp")
    parser.add_argument("--page-size", type=int, choices=range(1,26), default=25)
    parser.add_argument("--next-token", help="Opaque Historian pagination token; single page only")
    parser.add_argument("--allow-documented-os-v1", action="store_true")
    args = parser.parse_args()
    try:
        path = build_path(args)
        result = request_json("GET", path, "Bearer " + get_token())
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
