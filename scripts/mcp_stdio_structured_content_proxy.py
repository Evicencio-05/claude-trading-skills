#!/usr/bin/env python3
"""
stdio MCP proxy: inject structuredContent for Cursor compatibility.

Some remote MCP servers return tool results in legacy ``content`` only while
advertising ``outputSchema``. Cursor rejects those responses. This script wraps
any stdio MCP child process and patches JSON-RPC response lines on stdout.

Usage:
    python3 scripts/mcp_stdio_structured_content_proxy.py -- <child> [child args...]

Example (.cursor/mcp.json):
    uv run python3 scripts/mcp_stdio_structured_content_proxy.py -- \\
        npx -y mcp-remote https://agent.robinhood.com/mcp/trading
"""

from __future__ import annotations

import json
import os
import select
import subprocess
import sys
import threading
from typing import Any


def _debug(msg: str) -> None:
    if os.environ.get("MCP_PROXY_DEBUG"):
        print(msg, file=sys.stderr, flush=True)


def _content_to_structured(content: list[Any]) -> dict[str, Any] | None:
    if not content:
        return None
    for item in content:
        if not isinstance(item, dict) or item.get("type") != "text":
            continue
        text = item.get("text", "")
        if not isinstance(text, str):
            return {"text": str(text)}
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return {"text": text}
        if isinstance(parsed, dict):
            return parsed
        return {"text": text}
    return None


def inject_structured_content(result: Any) -> Any:
    """Add structuredContent to a tools/call result when missing."""
    if not isinstance(result, dict):
        return result
    if result.get("structuredContent") is not None:
        return result
    content = result.get("content")
    if not content:
        return result
    structured = _content_to_structured(content)
    if structured is None:
        return result
    return {**result, "structuredContent": structured}


def patch_jsonrpc_line(line: str) -> str:
    """Patch one stdout line from the child MCP server."""
    stripped = line.strip()
    if not stripped:
        return line
    try:
        message = json.loads(stripped)
    except json.JSONDecodeError:
        return line
    if not isinstance(message, dict):
        return line
    if "result" not in message or "error" in message:
        return line
    result = message.get("result")
    if not isinstance(result, dict):
        return line
    patched_result = inject_structured_content(result)
    if patched_result is result:
        return line
    message = {**message, "result": patched_result}
    return json.dumps(message, separators=(",", ":")) + ("\n" if line.endswith("\n") else "")


def _relay_stdin_to_child(child: subprocess.Popen[bytes]) -> None:
    """Forward parent stdin to child stdin until EOF (runs in a thread)."""
    assert child.stdin is not None
    try:
        while True:
            if hasattr(select, "select"):
                ready, _, _ = select.select([sys.stdin], [], [], 0.05)
                if not ready:
                    if child.poll() is not None:
                        break
                    continue
            chunk = sys.stdin.buffer.read1(4096)
            if not chunk:
                break
            child.stdin.write(chunk)
            child.stdin.flush()
    except (BrokenPipeError, OSError):
        pass
    finally:
        try:
            child.stdin.close()
        except OSError:
            pass


def _relay_child_stdout_to_parent(child: subprocess.Popen[bytes]) -> None:
    """Forward child stdout to parent stdout, patching JSON-RPC lines."""
    assert child.stdout is not None
    buffer = b""
    while True:
        chunk = child.stdout.read(4096)
        if not chunk:
            if buffer:
                line = buffer.decode(errors="replace")
                sys.stdout.write(patch_jsonrpc_line(line))
                sys.stdout.flush()
            break
        buffer += chunk
        while b"\n" in buffer:
            raw_line, buffer = buffer.split(b"\n", 1)
            line = raw_line.decode(errors="replace") + "\n"
            sys.stdout.write(patch_jsonrpc_line(line))
            sys.stdout.flush()


def _relay_bidirectional(child: subprocess.Popen[bytes]) -> None:
    """MCP stdio requires concurrent stdin/stdout relay; sequential relay deadlocks."""
    stdout_thread = threading.Thread(
        target=_relay_child_stdout_to_parent,
        args=(child,),
        name="mcp-proxy-stdout",
        daemon=True,
    )
    stdout_thread.start()
    _relay_stdin_to_child(child)
    stdout_thread.join()


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    if not args or args[0] != "--":
        print(
            "Usage: mcp_stdio_structured_content_proxy.py -- <child> [child args...]",
            file=sys.stderr,
        )
        return 1
    child_cmd = args[1:]
    if not child_cmd:
        print("Error: missing child command after --", file=sys.stderr)
        return 1

    _debug(f"spawning child: {child_cmd!r}")
    child = subprocess.Popen(
        child_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
    )
    try:
        _relay_bidirectional(child)
        return child.wait()
    except KeyboardInterrupt:
        child.terminate()
        try:
            child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            child.kill()
        return 130
    finally:
        if child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=2)
            except subprocess.TimeoutExpired:
                child.kill()


if __name__ == "__main__":
    raise SystemExit(main())
