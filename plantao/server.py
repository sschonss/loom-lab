#!/usr/bin/env python3
"""MCP mínimo do plantão. A resposta mora no roster, não na memória do Loom."""

import json
import sys
from pathlib import Path

ROSTER = Path(__file__).with_name("roster.json")


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
    return json.loads(ROSTER.read_text())


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
                            "description": "Devolve quem está de plantão agora, segundo o roster do serviço.",
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
                    "error": {"code": -32602, "message": "ferramenta desconhecida"},
                }
            )
            return
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {"type": "text", "text": json.dumps(plantonista(), ensure_ascii=False)}
                    ]
                },
            }
        )
        return
    if msg_id is not None:
        send(
            {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": "método não tratado"},
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
