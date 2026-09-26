# Product Name Mapping

The platform formerly known as "Vertex AI" is now **Gemini Enterprise Agent Platform** (short: **Agent Platform**). Users may refer to products by different names. Map them to the correct CLI values:

| User may say | CLI value |
|-------------|-----------|
| Agent Engine, Vertex AI Agent Engine, Agent Runtime | `--deployment-target agent_runtime` |
| Agent Engine sessions, Agent Platform Sessions | `--session-type agent_platform_sessions` |
| Vertex AI Search, Vertex AI Vector Search, RAG | clone-and-study recipe, not a flag (see `/google-agents-cli-adk-code` → `references/samples.md`) |

`google-cloud-aiplatform`, ships two importable packages: the older `vertexai` and the newer
`agentplatform`. New code should import `agentplatform`.
