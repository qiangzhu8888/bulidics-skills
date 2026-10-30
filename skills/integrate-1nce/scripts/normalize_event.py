"""Normalize a single Cloud Integrator event from stdin; no auth, persistence or model decoder."""
import base64
import binascii
import json
import sys
from datetime import datetime, timezone

def normalize(event):
    if not isinstance(event, dict):
        raise ValueError("Expected a single Cloud Integrator event object")
    event_id = event.get("id")
    if not isinstance(event_id, str) or not event_id:
        raise ValueError("Missing event id")
    if event.get("type") == "TEST_MESSAGE":
        return {"kind": "test", "event_id": event_id}
    if event.get("type") != "TELEMETRY_DATA":
        raise ValueError("Unsupported event type; route separately")
    device = event.get("device")
    iccid = device.get("iccid") if isinstance(device, dict) else None
    if not isinstance(iccid, str) or not iccid:
        raise ValueError("ICCID must be a nonempty string")
    stamp = event.get("received")
    if isinstance(stamp, bool) or not isinstance(stamp, (str, int)) or not str(stamp).isdigit():
        raise ValueError("received must be UNIX milliseconds")
    try:
        received = datetime.fromtimestamp(int(stamp) / 1000, timezone.utc).isoformat()
    except (ValueError, OverflowError, OSError):
        raise ValueError("Invalid received timestamp") from None
    payload = event.get("payload")
    if not isinstance(payload, dict) or "value" not in payload:
        raise ValueError("Missing payload.value")
    encoding = payload.get("encoding")
    value = payload["value"]
    if encoding == "base64":
        if not isinstance(value, str):
            raise ValueError("Base64 payload must be a string")
        try:
            raw = base64.b64decode(value, validate=True)
        except (ValueError, binascii.Error):
            raise ValueError("Invalid Base64 payload") from None
        data = {"raw_hex": raw.hex()}
        quality = "decoder_required"
    elif encoding is not None:
        raise ValueError("Unknown payload encoding")
    elif payload.get("type") == "JSON":
        if not isinstance(value, (dict, list)):
            raise ValueError("JSON payload.value must be an object or array")
        data = value
        quality = "mapping_required"
    elif payload.get("type") == "STRING" and isinstance(value, str):
        data = {"raw_text": value}
        quality = "decoder_required"
    else:
        raise ValueError("Unsupported payload format")
    return {"kind": "telemetry", "provider": "1nce", "event_id": event_id,
            "iccid": iccid, "received_at": received, "measured_at": None,
            "data": data, "quality_status": quality}

def main():
    try:
        raw = sys.stdin.buffer.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError("Input exceeds 1 MiB")
        def invalid_constant(value):
            raise ValueError("Nonfinite JSON number")
        result = normalize(json.loads(raw, parse_constant=invalid_constant))
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except (ValueError, UnicodeError):
        print("Invalid or unsupported Cloud Integrator event", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
