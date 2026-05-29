"""Robinhood MCP client via one-shot stdio session (proxy + local mcp-remote)."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_STDIO_LAUNCHER = _REPO_ROOT / "scripts" / "run_robinhood_mcp_stdio.sh"


class RobinhoodMcpError(RuntimeError):
    pass


def _run_stdio_session(
    outbound_lines: list[dict[str, Any]],
    timeout: float = 35.0,
    settle_seconds: float = 5.0,
) -> list[dict[str, Any]]:
    """Spawn one MCP stdio session, send JSON-RPC lines, return parsed responses."""
    if not _STDIO_LAUNCHER.is_file():
        raise RobinhoodMcpError(
            f"Missing {_STDIO_LAUNCHER}. Run: bash scripts/setup_robinhood_mcp.sh"
        )

    payload = "\n".join(json.dumps(m, separators=(",", ":")) for m in outbound_lines) + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as tmp:
        tmp.write(payload)
        req_path = tmp.name

    cmd = (
        f"(sleep 0.3; cat '{req_path}'; sleep {settle_seconds}) "
        f"| bash scripts/run_robinhood_mcp_stdio.sh"
    )
    try:
        try:
            proc = subprocess.run(
                ["bash", "-c", cmd],
                cwd=str(_REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as e:
            raise RobinhoodMcpError(f"MCP session timed out after {timeout}s") from e
    finally:
        Path(req_path).unlink(missing_ok=True)

    if proc.returncode != 0 and not proc.stdout.strip():
        err = (proc.stderr or "").strip()[-500:]
        raise RobinhoodMcpError(f"MCP session failed (exit {proc.returncode}): {err}")

    responses: list[dict[str, Any]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict) and "id" in msg and ("result" in msg or "error" in msg):
            responses.append(msg)
    return responses


def _session_with_init(
    tool_calls: list[tuple[str, dict[str, Any]]],
    timeout: float = 35.0,
) -> list[dict[str, Any]]:
    lines: list[dict[str, Any]] = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "robinhood_mcp_cli", "version": "1.0"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
    ]
    msg_id = 2
    for name, args in tool_calls:
        lines.append(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "method": "tools/call",
                "params": {"name": name, "arguments": args},
            }
        )
        msg_id += 1
    return _run_stdio_session(lines, timeout=timeout)


def call_tool(
    name: str,
    arguments: dict[str, Any] | None = None,
    timeout: float = 35.0,
) -> dict[str, Any]:
    responses = _session_with_init([(name, arguments or {})], timeout=timeout)
    if not responses:
        raise RobinhoodMcpError(f"{name}: no response")
    # Last response is the tool call (id=2)
    resp = responses[-1]
    if "error" in resp:
        raise RobinhoodMcpError(f"{name} failed: {resp['error']}")
    result = resp.get("result", {})
    if not isinstance(result, dict):
        raise RobinhoodMcpError(f"{name}: invalid result")
    return result


def call_tools(
    calls: list[tuple[str, dict[str, Any]]],
    timeout: float = 60.0,
) -> list[dict[str, Any]]:
    responses = _session_with_init(calls, timeout=timeout)  # noqa: same name
    # Skip initialize response (id=1); return tool results only
    return [r for r in responses if r.get("id", 0) >= 2]


def tool_data(
    name: str, arguments: dict[str, Any] | None = None, timeout: float = 35.0
) -> dict[str, Any]:
    result = call_tool(name, arguments, timeout=timeout)
    structured = result.get("structuredContent")
    if isinstance(structured, dict):
        return structured
    content = result.get("content")
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = item.get("text", "")
                if isinstance(text, str):
                    try:
                        parsed = json.loads(text)
                        if isinstance(parsed, dict):
                            return parsed
                    except json.JSONDecodeError:
                        pass
    raise RobinhoodMcpError(f"{name}: no structured data in response")


class RobinhoodMcpClient:
    """Context manager shim for robinhood_mcp.py."""

    def __init__(self, timeout: float = 35.0) -> None:
        self.timeout = timeout

    def __enter__(self) -> RobinhoodMcpClient:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def tool_data(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        return tool_data(name, arguments, timeout=self.timeout)


def extract_accounts(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data", payload)
    accounts = data.get("accounts") if isinstance(data, dict) else None
    if not isinstance(accounts, list):
        return []
    return [a for a in accounts if isinstance(a, dict)]


def extract_positions(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data", payload)
    positions = data.get("positions") if isinstance(data, dict) else None
    if not isinstance(positions, list):
        return []
    return [p for p in positions if isinstance(p, dict)]
