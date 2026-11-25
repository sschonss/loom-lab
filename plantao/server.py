#!/usr/bin/env python3
"""Thin on-call MCP. The answer comes from the Mockoon HTTP mock."""

import json
import os
import sys
import urllib.error
import urllib.request

PLANTAO_URL = os.environ.get("PLANTAO_URL", "http://127.0.0.1:3010/plantonista")


def send(message: dict) -> None:
    body = json.dumps(message).encode()
    header = f"Content-Length: {len(body)}\r\n\r\n".encode()
    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()


def read_message():
    headers = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, value = line.decode().split(":", 1)
        headers[key.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length == 0:
        return None
    return json.loads(sys.stdin.buffer.read(length))


def plantonista() -> dict:
    request = urllib.request.Request(PLANTAO_URL, method="GET")
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode())


def handle(message: dict) -> None:
    method = message.get("method")
    msg_id = message.get("id")
    if method == "initialize":
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "plantao", "version": "0.1.0"},
                },
            }
        )
        return
    if method == "notifications/initialized":
        return
    if method == "tools/list":
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "plantonista_de_hoje",
                            "description": "Returns who is on call right now, according to the service roster.",
                            "inputSchema": {"type": "object", "properties": {}},
                        }
                    ]
                },
            }
        )
        return
    if method == "tools/call":
        name = message.get("params", {}).get("name")
        if name != "plantonista_de_hoje":
            send(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32602, "message": "unknown tool"},
                }
            )
            return
        try:
            body = plantonista()
            send(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(body, ensure_ascii=False),
                            }
                        ]
                    },
                }
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            send(
                {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "isError": True,
                        "content": [
                            {
                                "type": "text",
                                "text": f"The on-call mock did not respond at {PLANTAO_URL}: {exc}",
                            }
                        ],
                    },
                }
            )
        return
    if msg_id is not None:
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": "method not handled"},
            }
        )


def main() -> None:
    while True:
        message = read_message()
        if message is None:
            return
        handle(message)


if __name__ == "__main__":
    main()
