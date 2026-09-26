# Batch Inference (Cloud Run)

Invoke your agent as a BigQuery Remote Function for batch inference over table rows. This requires a custom `POST /` endpoint since BQ cannot use URL paths.

> **ADK projects.** The BigQuery request/response contract and the Terraform below apply to any framework; both handlers invoke the agent through the ADK `Runner`, so swap in your framework's invocation. For the `Runner` API, see `/google-agents-cli-adk-code`.

> For event-driven triggers (Pub/Sub, Eventarc): ADK Python has native `trigger_sources`. ADK Go has `pubsub` and `eventarc` sub-launchers, which the scaffolded entrypoint does not start. See: `/google-agents-cli-adk-code`

## BigQuery Remote Function

### Python handler

BQ sends `{"calls": [["row1"], ...], "caller": "..."}`, expects `{"replies": ["...", ...]}` in same order. BQ **cannot use URL paths** — register at `POST /`.

```python
import asyncio, json, uuid
from fastapi import Request
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from my_agent.agent import root_agent

APP_NAME = "my_agent"
_trigger_session_service = InMemorySessionService()
_trigger_runner = Runner(
    agent=root_agent, app_name=APP_NAME, session_service=_trigger_session_service,
)

async def _run_agent(message_text: str, user_id: str = "trigger") -> list:
    session = await _trigger_session_service.create_session(
        app_name=APP_NAME, user_id=user_id, session_id=str(uuid.uuid4())
    )
    events = []
    async for event in _trigger_runner.run_async(
        user_id=user_id, session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part(text=message_text)]),
    ):
        events.append(event)
    return events

@app.post("/")
async def trigger_bq(request: Request):
    body = await request.json()
    calls: list = body.get("calls", [])
    user_id = body.get("caller") or body.get("sessionUser") or "bq"

    async def _process_row(row_args: list) -> str:
        text = row_args[0] if (len(row_args) == 1 and isinstance(row_args[0], str)) \
               else json.dumps(row_args)
        try:
            events = await _run_agent(text, user_id=user_id)
            return json.dumps([e.model_dump(mode="json") for e in events])
        except Exception as e:
            return f"Error: {e}"

    replies = await asyncio.gather(*[_process_row(row) for row in calls])
    return {"replies": list(replies)}
```

### Go handler

A Go project has no FastAPI app to hang a route on. Serve the BigQuery endpoint from your own mux
with `adkrest.Server` mounted beside it — the composition upstream's
[`examples/rest`](https://github.com/google/adk-go/tree/main/examples/rest) uses, and the one
`/google-agents-cli-adk-code` (`references/adk-go.md`) covers in full.

```go
restServer, _ := adkrest.NewServer(adkrest.ServerConfig{
	AgentLoader:     agent.NewSingleLoader(rootAgent),
	SessionService:  session.InMemoryService(),
	SSEWriteTimeout: 120 * time.Second,
})

mux := http.NewServeMux()

// "POST /{$}" matches the root path exactly, so it does not shadow the ADK
// routes mounted at "/" below, and registration order does not matter.
mux.HandleFunc("POST /{$}", func(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Calls [][]any `json:"calls"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	replies := make([]string, 0, len(req.Calls))
	for _, call := range req.Calls {
		prompt := ""
		if len(call) > 0 {
			prompt = fmt.Sprint(call[0])
		}
		// Invoke the agent here via runner.Runner; see /google-agents-cli-adk-code.
		replies = append(replies, prompt)
	}
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]any{"replies": replies})
})

mux.Handle("/", restServer)
http.ListenAndServe(addr, mux)
```

This replaces the launcher, so `webui` and the keyword CLI go away; mount `server/adka2a` and
`server/agentengine` on the same mux if you need them.

Add the package to the image too — the generated `Dockerfile` copies **named** directories, so a new
one is absent from the build context and the build fails with `package <mod>/<pkg> is not in std`:

```dockerfile
COPY bqremote/ ./bqremote/
```

### BQ remote function Terraform:

```hcl
resource "google_bigquery_routine" "my_fn" {
  routine_type    = "SCALAR_FUNCTION"
  language        = "SQL"
  definition_body = ""
  arguments {
    name          = "message"
    argument_kind = "FIXED_TYPE"
    data_type     = jsonencode({ typeKind = "STRING" })
  }
  return_type = jsonencode({ typeKind = "STRING" })
  remote_function_options {
    endpoint   = google_cloud_run_v2_service.app.uri  # root URL only
    connection = google_bigquery_connection.my_conn.name
  }
}
```
