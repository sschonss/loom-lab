#!/bin/sh
set -eu

base_url="${LOOM_BASE_URL:-http://localhost:7777}"

post() {
  curl -fsS -X POST "$base_url/v1/memory.set" \
    -H 'Content-Type: application/json' \
    -d "$1"
  printf '\n'
}

post '{"memory_key":"team/deploy-window","value":"A janela de deploy do time é terça e quinta, às 16h."}'
post '{"memory_key":"team/oncall-lookup","value":"O nome do plantonista não fica nesta memória. Chame a ferramenta plantonista_de_hoje do servidor MCP plantao e responda com o JSON que ela devolver."}'
