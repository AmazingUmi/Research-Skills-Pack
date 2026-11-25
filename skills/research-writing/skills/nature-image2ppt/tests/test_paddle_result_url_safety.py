"""Offline result-address and transport checks."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

RUNTIME = Path(__file__).resolve().parents[1] / "cli" / "image2ppt" / "runtime"
sys.path.insert(0, str(RUNTIME))
import paddle_text_hints as paddle


class ResultUrlSafetyTests(unittest.TestCase):
    def test_plaintext_and_non_public_addresses_are_rejected_before_connect(self):
        for url, ip in [("http://example.test/file", "8.8.8.8"),
                        ("https://example.test/file", "127.0.0.1"),
                        ("https://example.test/file", "100.100.100.200")]:
            with self.subTest(url=url, ip=ip), patch.object(paddle.socket, "getaddrinfo",
                    return_value=[(2, 1, 6, "", (ip, 443))]), patch.object(paddle.http.client, "HTTPSConnection") as connect:
                with self.assertRaises(RuntimeError):
                    paddle.fetch_result_text(url)
                connect.assert_not_called()

    def test_tls_host_and_connection_address_are_bound_and_redirects_rejected(self):
        for status in (200, 302):
            with self.subTest(status=status), patch.object(paddle.socket, "getaddrinfo",
                    return_value=[(2, 1, 6, "", ("8.8.8.8", 443))]) as dns, patch.object(
                    paddle.http.client, "HTTPSConnection") as connect, patch.object(paddle.socket, "create_connection") as dial:
                conn = connect.return_value
                conn.getresponse.return_value.status = status
                conn.getresponse.return_value.read.return_value = b"fixture"
                if status == 200:
                    self.assertEqual(paddle.fetch_result_text("https://result.test/path?q=1"), "fixture")
                else:
                    with self.assertRaisesRegex(RuntimeError, "redirects"):
                        paddle.fetch_result_text("https://result.test/path?q=1")
                connect.assert_called_once_with("result.test", 443, timeout=60)
                conn.request.assert_called_once_with("GET", "/path?q=1")
                conn._create_connection(("result.test", 443), 60)
                dial.assert_called_once_with(("8.8.8.8", 443), 60)
                dns.assert_called_once()
