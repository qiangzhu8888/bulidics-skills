#!/usr/bin/env python3
"""Offline helpers for ZETA Server HTTP signing and MQTT dataDetail parsing."""
import argparse
import hashlib
import hmac
import json
import time


def sign(api_key, secret_key, request_time=None):
    ts = int(time.time()) if request_time is None else int(request_time)
    signature = hmac.new(f"{secret_key}{ts}".encode(), api_key.encode(), hashlib.sha1).hexdigest()
    return {"request_time": ts, "signal": signature}


def decode(message):
    if not isinstance(message, dict):
        raise ValueError("MQTT payload must be a JSON object")
    result = dict(message)
    if isinstance(result.get("dataDetail"), str):
        result["dataDetail"] = json.loads(result["dataDetail"])
    return result


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("sign")
    p.add_argument("--api-key", required=True)
    p.add_argument("--secret-key", required=True)
    p.add_argument("--request-time", type=int)
    p = sub.add_parser("decode")
    p.add_argument("--json", required=True)
    args = parser.parse_args()
    if args.command == "sign":
        print(json.dumps(sign(args.api_key, args.secret_key, args.request_time)))
    else:
        print(json.dumps(decode(json.loads(args.json)), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
