# Loom lab

One base, two editors. The person in Cursor and the person in OpenCode ask the same questions and get the same answer. The lab starts small and grows in stages.

The test write-up, with screenshots, is in [docs/how-it-works.md](docs/how-it-works.md). That text is the base for the article.

## Stage 1, now

Two questions.

**What is the deploy window?** The answer is text in Loom, at `work/decision/deploy-window`: Monday to Friday, 08:00 to 14:00.

**Who is on call today?** Memory does not store the name. The key `work/procedure/plantonista-de-hoje` only says which tool to call. The agent calls `plantonista_de_hoje` on the `plantao` MCP. That tool sends a GET to `http://127.0.0.1:3010/plantonista`, and Mockoon answers with the body in `mockoon/plantao.json`. To change who is on call, edit that file and recreate the container.

## Stage 2, later

Questions that need more than a paragraph. For example: "how do I find this log in production?". Memory then describes the path: which MCP to call, which tool, and what has to be configured on the machine. This stage is not built. The same shape covers the deploy process and which dashboards to watch when deploying a given service.

## Start

Docker with Compose 2.20 or newer, and port 7777 free. Run the installer from your home directory:

```bash
curl -fsSL https://github.com/ClickHouse/loom/releases/latest/download/install.sh -o loom-install.sh \
  && sh loom-install.sh && rm loom-install.sh
```

Dashboard at http://localhost:7777/.

Start the on-call mock. Port 3000 on this machine already has another service, so Mockoon listens on 3010:

```bash
docker compose up -d
```

Check with `curl -s http://127.0.0.1:3010/plantonista`. Then store the two stage 1 memories:

```bash
sh scripts/seed-memory.sh
```

The 24 November 2026 test wrote those memories in Portuguese, from the chats, and did not use this script. The script writes the same keys in English. Running it replaces the value at each key.

To stop, without deleting memories:

```bash
docker compose --project-directory "$HOME/.loom" down
```

## Connect both editors

Both point at the same Loom URL and the same on-call server. The fragment is in `clients/mcp.json`. The on-call `args` use this repository's path.

In Cursor, merge that fragment into `~/.cursor/mcp.json`. The editor rule is in `.cursor/rules/loom.mdc`.

In OpenCode, in `~/.config/opencode/opencode.json`, Loom is a remote server and on-call is a local server:

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

Open this folder in both. Reload each one. In OpenCode, ask the two stage 1 questions. The deploy window comes from Loom. The on-call person comes from the service.

## What this mode does not separate

Anyone who can reach `localhost:7777` reads and writes the same base. That is enough for two editors on this machine. A team on different machines uses an account, a namespace, and a token per person: [Tokens and grants](https://loom.clickhouse.com/docs/guides/tokens-and-grants).
