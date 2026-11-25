## Loom: shared team memory

Loom is connected as an MCP server. Its tools are named `loom_*`.

Before answering, call `loom_context_pack` with the question as `query`. If the pack does not contain the fact, call `loom_search`.

- "What is the deploy window?" Answer with the text of memory `work/decision/deploy-window`.
- "Who is on call today?" Do not invent a name. Memory `work/procedure/plantonista-de-hoje` only stores the path. Follow it and call `plantonista_de_hoje` on the MCP server `plantao`. The answer is the Mockoon JSON, not an invented name.

When the person states a team decision or a correction, save it with `loom_memory_set`, one fact per key `work/<topic>`. Do not save a guess or the transcript.
