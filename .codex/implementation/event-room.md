# Event and Chat Rooms

`EventRoom` presents deterministic text events with selectable outcomes. Each
option applies its effect immediately and the scene returns to the map without
consuming a room on the floor.

`ChatRoom` offers optional one-message conversations after battles. It uses a
local HuggingFace pipeline via LangChain and remembers dialogue history per
character for the duration of a run. By default the client loads the
`microsoft/phi-2` model unless `AUTOFIGHTER_LLM_MODEL` specifies another. The
room only appears when both `langchain-huggingface` and `transformers` are
installed. Players may skip the chat; skipping returns to the map without
counting toward the per-floor chat limit of six.

