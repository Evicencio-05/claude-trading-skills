"""Tests for local_llm.py and local_llm_cli.py."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml


def _load_module(name: str, script_path: Path):
    spec = importlib.util.spec_from_file_location(name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def local_llm():
    path = Path(__file__).resolve().parents[1] / "local_llm.py"
    return _load_module("local_llm", path)


@pytest.fixture(scope="module")
def local_llm_cli():
    path = Path(__file__).resolve().parents[1] / "local_llm_cli.py"
    return _load_module("local_llm_cli", path)


def _mock_response(data: dict, status: int = 200):
    body = json.dumps(data).encode("utf-8")
    resp = MagicMock()
    resp.read.return_value = body
    resp.status = status
    resp.__enter__ = MagicMock(return_value=resp)
    resp.__exit__ = MagicMock(return_value=False)
    return resp


def test_load_config_defaults(local_llm, monkeypatch):
    monkeypatch.delenv("OLLAMA_HOST", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    cfg = local_llm.load_config(Path("/nonexistent"))
    assert cfg["host"] == "http://127.0.0.1:11434"
    assert cfg["model"] == "qwen2.5:7b"


def test_load_config_env_override(local_llm, monkeypatch):
    monkeypatch.setenv("OLLAMA_HOST", "http://localhost:9999")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3:8b")
    cfg = local_llm.load_config(Path("/nonexistent"))
    assert cfg["host"] == "http://localhost:9999"
    assert cfg["model"] == "llama3:8b"


def test_is_available_true(local_llm):
    tags = {"models": [{"name": "qwen2.5:7b"}, {"name": "llama3:8b"}]}
    with patch("urllib.request.urlopen", return_value=_mock_response(tags)):
        assert (
            local_llm.is_available({"host": "http://127.0.0.1:11434", "model": "qwen2.5:7b"})
            is True
        )


def test_is_available_false_no_model(local_llm):
    tags = {"models": [{"name": "llama3:8b"}]}
    with patch("urllib.request.urlopen", return_value=_mock_response(tags)):
        assert (
            local_llm.is_available({"host": "http://127.0.0.1:11434", "model": "qwen2.5:7b"})
            is False
        )


def test_is_available_connection_error(local_llm):
    with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
        assert (
            local_llm.is_available({"host": "http://127.0.0.1:11434", "model": "qwen2.5:7b"})
            is False
        )


def test_chat_returns_content(local_llm, tmp_path):
    cfg = {"host": "http://127.0.0.1:11434", "model": "qwen2.5:7b", "timeout_seconds": 30}
    chat_resp = {"message": {"content": "Hello from Ollama"}}
    with patch("urllib.request.urlopen", return_value=_mock_response(chat_resp)):
        result = local_llm.chat("Say hi", config=cfg, repo_root=tmp_path, task="test")
    assert result == "Hello from Ollama"


def test_extract_json_from_text(local_llm):
    text = 'Here is output:\n{"candidates": [{"title": "foo"}]}'
    obj = local_llm.extract_json_from_text(text, ["candidates"])
    assert obj is not None
    assert obj["candidates"][0]["title"] == "foo"


def test_build_edge_hints_prompt(local_llm):
    payload = {"as_of": "2026-05-31", "anomalies": [], "instruction": "Generate hints"}
    prompt = local_llm.build_edge_hints_prompt(payload)
    assert "2026-05-31" in prompt
    assert "YAML" in prompt or "yaml" in prompt.lower()


def test_cli_health_unavailable(local_llm_cli, monkeypatch):
    monkeypatch.setattr(
        local_llm_cli, "load_config", lambda _root: {"host": "http://x", "model": "m"}
    )
    monkeypatch.setattr(local_llm_cli, "is_available", lambda _cfg, _root=None: False)
    assert local_llm_cli.cmd_health(Path(".")) == 2


def test_cli_health_ok(local_llm_cli, monkeypatch):
    monkeypatch.setattr(
        local_llm_cli, "load_config", lambda _root: {"host": "http://x", "model": "m"}
    )
    monkeypatch.setattr(local_llm_cli, "is_available", lambda _cfg, _root=None: True)
    assert local_llm_cli.cmd_health(Path(".")) == 0


def test_cmd_edge_hints_parses_output(local_llm_cli, monkeypatch, tmp_path):
    hints_yaml = yaml.safe_dump(
        {"hints": [{"title": "Test hint", "observation": "Risk-on breadth"}]}
    )
    monkeypatch.setattr(
        local_llm_cli,
        "chat_or_raise",
        lambda *args, **kwargs: f"```yaml\n{hints_yaml}```",
    )
    payload = json.dumps({"as_of": "2026-05-31", "anomalies": []})
    with patch("sys.stdin", io.StringIO(payload)):
        code = local_llm_cli.cmd_edge_hints(tmp_path)
    assert code == 0


def test_cmd_commit_message_no_staged(local_llm_cli, monkeypatch, tmp_path):
    monkeypatch.setattr(
        local_llm_cli.subprocess,
        "run",
        lambda *a, **k: MagicMock(returncode=0, stdout=""),
    )
    assert local_llm_cli.cmd_commit_message(tmp_path) == 1
