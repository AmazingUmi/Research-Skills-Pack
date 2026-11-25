from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


ROOT = Path(__file__).resolve().parents[1]
CLI_DIR = ROOT / "cli"
sys.path.insert(0, str(CLI_DIR))

from image2ppt.runtime import runtime_env  # noqa: E402


class RuntimeConfigTests(unittest.TestCase):
    def test_saved_oauth_preference_does_not_authorize_a_credential_read(self):
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
            runtime_env, "read_config_file", return_value={"IMAGE2PPT_IMAGE_BACKEND": "codex-oauth"}
        ), mock.patch.object(runtime_env, "codex_oauth_ready", return_value=True) as read_oauth:
            for options in ({}, {"check_api": True}, {"backend": "auto"}, {"backend": "openai-compatible-api"}):
                status = runtime_env.collect_status(**options)
                self.assertFalse(status["image_backend"]["codex_oauth"]["checked"])
            read_oauth.assert_not_called()
            status = runtime_env.collect_status(backend="codex-oauth")
            read_oauth.assert_called_once_with()
            self.assertTrue(status["image_backend"]["cli_fallback_ready"])

    def test_public_doctor_and_setup_forward_only_explicit_oauth_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config = home / "config.yaml"
            config.write_text("IMAGE2PPT_IMAGE_BACKEND: codex-oauth\n", encoding="utf-8")
            auth = home / "fixture-auth.json"
            auth.write_text(json.dumps({"tokens": {"access_token": "fixture-value"}}), encoding="utf-8")
            env = {**os.environ, "IMAGE2PPT_CONFIG_HOME": directory, "CODEX_AUTH_FILE": str(auth)}
            for key in runtime_env.ENV_FIELDS:
                env.pop(key, None)
            for command in ("doctor", "setup"):
                for explicit in (False, True):
                    with self.subTest(command=command, explicit=explicit):
                        argv = [sys.executable, str(runtime_env.CLI_ENTRY), command, "--check-api"]
                        if command == "doctor":
                            argv.append("--json")
                        if explicit:
                            argv.extend(["--backend", "codex-oauth"])
                        result = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=30)
                        payload = json.loads(result.stdout)
                        status = payload["doctor"] if command == "setup" else payload
                        self.assertEqual(0 if status["ok"] else 1, result.returncode)
                        oauth = status["image_backend"]["codex_oauth"]
                        self.assertEqual(explicit, oauth["checked"])
                        self.assertIs(oauth["ready"], True if explicit else None)
                        self.assertEqual(explicit, status["image_backend"]["cli_fallback_ready"])
                        self.assertNotIn("fixture-value", result.stdout + result.stderr)

    def test_local_and_cloud_readiness_have_distinct_dependencies(self):
        mods = {name: {"available": name not in ("openai", "requests")} for name in runtime_env.module_status()}
        with mock.patch.object(runtime_env, "module_status", return_value=mods), mock.patch.object(
            runtime_env, "renderer_status", return_value={"ready": True}
        ), mock.patch.object(runtime_env, "font_status", return_value={"ready": True}), mock.patch.object(
            runtime_env, "read_config_file", return_value={}
        ), mock.patch.dict(os.environ, {"PADDLE_OCR_TOKEN": "fixture", "OPENAI_API_KEY": "fixture",
                                        "IMAGE2PPT_IMAGE_BACKEND": "auto"}), mock.patch.object(
            runtime_env, "codex_oauth_ready", side_effect=AssertionError("unexpected OAuth lookup")
        ):
            self.assertTrue(runtime_env.collect_status()["ok"])
            self.assertFalse(runtime_env.collect_status(check_api=True)["ok"])
            self.assertFalse(runtime_env.collect_status(check_ocr=True)["ok"])
            mods["requests"]["available"] = True
            self.assertTrue(runtime_env.collect_status(check_ocr=True)["ok"])
            mods["defusedxml"]["available"] = False
            self.assertFalse(runtime_env.collect_status()["ok"])

    def test_update_restricts_existing_config_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.yaml"
            config.write_text("OPENAI_API_KEY: old-key\n", encoding="utf-8")
            if sys.platform != "win32":
                os.chmod(config, 0o644)

            runtime_env.write_config_file(config, {"OPENAI_API_KEY": "new-key"})

            self.assertEqual(
                runtime_env.read_config_file(config),
                {"OPENAI_API_KEY": "new-key"},
            )
            if sys.platform != "win32":
                self.assertEqual(config.stat().st_mode & 0o777, 0o600)

    def test_failed_serialization_preserves_existing_config(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "config.yaml"
            original = "OPENAI_API_KEY: existing-key\n"
            config.write_text(original, encoding="utf-8")

            with mock.patch.object(yaml, "safe_dump", side_effect=RuntimeError("write failed")):
                with self.assertRaisesRegex(RuntimeError, "write failed"):
                    runtime_env.write_config_file(config, {"OPENAI_API_KEY": "replacement-key"})

            self.assertEqual(config.read_text(encoding="utf-8"), original)
            self.assertEqual(list(config.parent.glob(f".{config.name}.*")), [])

    def test_failed_flush_or_replace_preserves_existing_config(self) -> None:
        for operation in ("fsync", "replace"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as directory:
                config = Path(directory) / "config.yaml"
                original = b"OPENAI_API_KEY: existing-key\n"
                config.write_bytes(original)

                with mock.patch.object(
                    runtime_env.os, operation, side_effect=OSError("disk error")
                ):
                    with self.assertRaisesRegex(OSError, "disk error"):
                        runtime_env.write_config_file(config, {"OPENAI_API_KEY": "new-key"})

                self.assertEqual(config.read_bytes(), original)
                self.assertEqual(list(config.parent.glob(f".{config.name}.*")), [])


if __name__ == "__main__":
    unittest.main()
