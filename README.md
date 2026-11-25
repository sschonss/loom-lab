# Laboratório Loom

Uma base só, dois editores. A pessoa no Cursor e a pessoa no OpenCode perguntam as mesmas coisas e recebem a mesma resposta. O laboratório começa pequeno e cresce por etapas.

## Etapa 1, agora

Duas perguntas.

**Qual é a janela de deploy?** A resposta é um texto na memória do Loom, na chave `team/deploy-window`: terça e quinta, às 16h.

**Quem é o plantonista do dia?** A memória não guarda o nome. A chave `team/oncall-lookup` só diz qual ferramenta chamar. O agente chama `plantonista_de_hoje` no MCP `plantao`, e a resposta sai de `plantao/roster.json`. Trocar a pessoa de plantão é editar esse arquivo. Os dois editores passam a ver o nome novo, sem mudar a memória.

## Etapa 2, depois

Perguntas que pedem mais do que um texto. Exemplo: "como identifico tal log em produção?". A memória passa a descrever o caminho: qual MCP chamar, qual ferramenta, e o que precisa estar configurado na máquina. Essa etapa ainda não está montada.

## Subir

Docker com Compose 2.20 ou mais novo, porta 7777 livre. Rode o instalador no seu diretório pessoal:

```bash
curl -fsSL https://github.com/ClickHouse/loom/releases/latest/download/install.sh -o loom-install.sh \
  && sh loom-install.sh && rm loom-install.sh
```

Dashboard em http://localhost:7777/. Grave as duas memórias da etapa 1:

```bash
sh scripts/seed-memory.sh
```

Para parar, sem apagar as memórias:

```bash
docker compose --project-directory "$HOME/.loom" down
```

## Ligar os dois editores

Os dois apontam para a mesma URL do Loom e para o mesmo servidor de plantão. O fragmento está em `clients/mcp.json`. O `args` do plantão usa o caminho deste repositório.

No Cursor, junte esse fragmento em `~/.cursor/mcp.json`. A regra do editor está em `.cursor/rules/loom.mdc`.

No OpenCode, em `~/.config/opencode/opencode.json`, o Loom entra como servidor remoto e o plantão como servidor local:

```json
{
  "mcp": {
    "servers": {
      "loom": {
        "type": "remote",
        "url": "http://localhost:7777/mcp?toolset=coding"
      },
      "plantao": {
        "type": "local",
        "command": ["python3", "plantao/server.py"]
      }
    }
  }
}
```

Abra esta pasta nos dois. Recarregue cada um. No OpenCode, pergunte as duas frases da etapa 1. A janela de deploy vem do Loom. O plantonista vem do serviço.

## O que este modo não separa

Quem alcança `localhost:7777` lê e grava a mesma base. Serve para os dois editores nesta máquina. Um time em máquinas diferentes usa conta, namespace e um token por pessoa: [Tokens and grants](https://loom.clickhouse.com/docs/guides/tokens-and-grants).
