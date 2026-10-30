import argparse
import copy
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit
from normalize_event import normalize
from read_1nce import build_path, get_token

class IntegrationExamples(unittest.TestCase):
    def setUp(self):
        self.event = {"id": "fixture-1", "type": "TELEMETRY_DATA", "received": "1793347200000", "device": {"iccid": "0012345678901234567"}, "payload": {"type": "JSON", "value": {"temperature": 24.6}}}

    def test_json_preserves_identity_and_does_not_invent_measurement_time(self):
        original = copy.deepcopy(self.event)
        result = normalize(self.event)
        self.assertEqual(result["iccid"], "0012345678901234567")
        self.assertIsNone(result["measured_at"])
        self.assertEqual(result["quality_status"], "mapping_required")
        self.assertEqual(self.event, original)

    def test_binary_requires_model_decoder(self):
        self.event["payload"] = {"type": "STRING", "encoding": "base64", "value": "AP8="}
        result = normalize(self.event)
        self.assertEqual(result["data"], {"raw_hex": "00ff"})
        self.assertEqual(result["quality_status"], "decoder_required")

    def test_test_event_needs_no_device(self):
        self.assertEqual(normalize({"id": "t", "type": "TEST_MESSAGE"})["kind"], "test")

    def test_reject_malformed_inputs(self):
        cases = [[], {**self.event, "device": {"iccid": 123}}, {**self.event, "received": True}, {**self.event, "payload": {"encoding": "base64", "value": "@@"}}, {**self.event, "type": "ERROR"}]
        for event in cases:
            with self.subTest(event=event), self.assertRaises(ValueError):
                normalize(event)

    def test_history_gate_and_url_encoding(self):
        args = argparse.Namespace(action="history", iccid="0012345678901234567", allow_documented_os_v1=False, page_size=25, start="2026-10-30T09:00:00+09:00", end=None, next_token="abc+/=")
        with self.assertRaises(ValueError):
            build_path(args)
        args.allow_documented_os_v1=True
        query = parse_qs(urlsplit(build_path(args)).query)
        self.assertEqual(query["startDateTime"], [args.start])
        self.assertEqual(query["nextToken"], [args.next_token])

    def test_token_not_returned_to_stdout(self):
        with patch.dict("os.environ", {"ONE_NCE_CLIENT_ID":"fixture-client", "ONE_NCE_CLIENT_SECRET":"fixture-secret"}), patch("read_1nce.request_json", return_value={"access_token":"fixture-token"}) as request:
            self.assertEqual(get_token(), "fixture-token")
            self.assertEqual(request.call_args.args[0:2], ("POST", "/oauth/token"))

if __name__ == "__main__":
    unittest.main()
