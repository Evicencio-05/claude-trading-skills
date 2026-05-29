"""Tests for mcp_stdio_structured_content_proxy."""

import json

from mcp_stdio_structured_content_proxy import (
    inject_structured_content,
    patch_jsonrpc_line,
)


def test_inject_parses_json_text_content():
    result = {
        "content": [{"type": "text", "text": '{"accounts": [{"account_number": "1234"}]}'}],
    }
    patched = inject_structured_content(result)
    assert patched["structuredContent"] == {"accounts": [{"account_number": "1234"}]}


def test_inject_plain_text_fallback():
    result = {"content": [{"type": "text", "text": "hello"}]}
    patched = inject_structured_content(result)
    assert patched["structuredContent"] == {"text": "hello"}


def test_inject_skips_when_structured_content_present():
    result = {
        "content": [{"type": "text", "text": '{"a": 1}'}],
        "structuredContent": {"a": 1},
    }
    patched = inject_structured_content(result)
    assert patched is result


def test_inject_skips_when_no_content():
    result = {"isError": False}
    patched = inject_structured_content(result)
    assert patched is result


def test_inject_skips_non_dict_result():
    assert inject_structured_content([]) == []


def test_patch_jsonrpc_line_response_with_content():
    line = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "content": [{"type": "text", "text": '{"ok": true}'}],
            },
        }
    )
    patched = patch_jsonrpc_line(line)
    data = json.loads(patched)
    assert data["result"]["structuredContent"] == {"ok": True}


def test_patch_jsonrpc_line_passthrough_non_json():
    assert patch_jsonrpc_line("not json") == "not json"


def test_patch_jsonrpc_line_passthrough_request():
    line = json.dumps({"jsonrpc": "2.0", "method": "initialize", "id": 1, "params": {}})
    assert patch_jsonrpc_line(line) == line


def test_patch_jsonrpc_line_passthrough_error():
    line = json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -1, "message": "fail"}})
    assert patch_jsonrpc_line(line) == line
