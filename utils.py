def serialize_agent_state(state):
    serialized = state.copy()

    # Convert messages to simple dicts
    serialized["messages"] = [
        {
            "type": type(m).__name__,
            "content": getattr(m, "content", str(m))
        }
        for m in serialized.get("messages", [])
    ]

    # Other fields are already simple (str)
    return serialized