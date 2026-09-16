from typing import Dict, List


class ShortTermMemory:

    def __init__(self):
        self.sessions: Dict[str, List[dict]] = {}

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:

        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(
        self,
        session_id: str,
    ) -> List[dict]:

        return self.sessions.get(session_id, []).copy()

    def clear(self, session_id: str) -> None:

        self.sessions.pop(session_id, None)