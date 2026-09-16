from src.memory.long_term import LongTermMemory
from src.memory.short_term import ShortTermMemory


def test_decision_is_saved_to_long_term_memory(
    tmp_path,
):

    database_path = tmp_path / "memory.db"

    short_term = ShortTermMemory()

    long_term = LongTermMemory(
        str(database_path)
    )

    decision = (
        "Further evaluation is recommended "
        "before expanding into Hyderabad."
    )

    short_term.add_message(
        "session_1",
        "assistant",
        decision,
    )

    long_term.save(
        "session_1",
        "decision",
        decision,
    )

    stored_decisions = long_term.retrieve(
        "session_1",
        "decision",
    )

    assert stored_decisions == [decision]