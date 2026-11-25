#!/bin/sh
set -eu

base_url="${LOOM_BASE_URL:-http://localhost:7777}"

post() {
  curl -fsS -X POST "$base_url/v1/memory.set" \
    -H 'Content-Type: application/json' \
    -d "$1"
  printf '\n'
}

post '{"memory_key":"work/decision/deploy-window","value":"The deploy window is Monday to Friday, from 08:00 to 14:00."}'
post '{"memory_key":"work/procedure/plantonista-de-hoje","value":"When someone asks who is on call, do not guess the name. Call the plantonista_de_hoje tool on the plantao MCP server and answer with exactly what that tool returns."}'
