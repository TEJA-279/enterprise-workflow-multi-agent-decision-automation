import sqlite3
from pathlib import Path


class LongTermMemory:

    def __init__(self, database_path: str = "memory.db"):

        self.database_path = Path(database_path)

        self._create_table()

    def _connect(self):

        return sqlite3.connect(self.database_path)

    def _create_table(self):

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    memory_key TEXT NOT NULL,
                    memory_value TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )

            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_session_key "
                "ON memories (session_id, memory_key, id)"
            )

            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_messages_session "
                "ON messages (session_id, id)"
            )

            connection.commit()

    def save(
        self,
        session_id: str,
        memory_key: str,
        memory_value: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO memories (
                    session_id,
                    memory_key,
                    memory_value
                )
                VALUES (?, ?, ?)
                """,
                (
                    session_id,
                    memory_key,
                    memory_value,
                ),
            )

            connection.commit()

    def retrieve(
        self,
        session_id: str,
        memory_key: str,
    ) -> list[str]:

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT memory_value
                FROM memories
                WHERE session_id = ?
                AND memory_key = ?
                ORDER BY id ASC
                """,
                (
                    session_id,
                    memory_key,
                ),
            )

            rows = cursor.fetchall()

        return [row[0] for row in rows]

    def delete(
        self,
        session_id: str,
        memory_key: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM memories
                WHERE session_id = ?
                AND memory_key = ?
                """,
                (
                    session_id,
                    memory_key,
                ),
            )

            connection.commit()

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO messages (session_id, role, content)
                VALUES (?, ?, ?)
                """,
                (session_id, role, content),
            )

    def retrieve_messages(
        self,
        session_id: str,
        limit: int = 40,
    ) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT role, content
                FROM messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()

        return [
            {"role": role, "content": content}
            for role, content in reversed(rows)
        ]