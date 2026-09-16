from src.memory.long_term import LongTermMemory


def test_long_term_memory_persists_data(tmp_path):

    database_path = tmp_path / "memory.db"

    memory = LongTermMemory(
        str(database_path)
    )

    memory.save(
        "session_1",
        "business_preference",
        "User is evaluating Hyderabad expansion.",
    )

    results = memory.retrieve(
        "session_1",
        "business_preference",
    )

    assert results == [
        "User is evaluating Hyderabad expansion."
    ]


def test_long_term_memory_survives_new_instance(tmp_path):

    database_path = tmp_path / "memory.db"

    memory_1 = LongTermMemory(
        str(database_path)
    )

    memory_1.save(
        "session_1",
        "decision",
        "Further evaluation is recommended.",
    )

    # Simulate application restart by creating
    # a completely new memory object.
    memory_2 = LongTermMemory(
        str(database_path)
    )

    results = memory_2.retrieve(
        "session_1",
        "decision",
    )

    assert results == [
        "Further evaluation is recommended."
    ]


def test_long_term_memory_isolated_by_session(tmp_path):

    database_path = tmp_path / "memory.db"

    memory = LongTermMemory(
        str(database_path)
    )

    memory.save(
        "session_1",
        "preference",
        "Hyderabad",
    )

    memory.save(
        "session_2",
        "preference",
        "Bangalore",
    )

    session_1 = memory.retrieve(
        "session_1",
        "preference",
    )

    session_2 = memory.retrieve(
        "session_2",
        "preference",
    )

    assert session_1 == ["Hyderabad"]
    assert session_2 == ["Bangalore"]


def test_conversation_messages_survive_new_instance(tmp_path):

    database_path = tmp_path / "memory.db"

    memory_1 = LongTermMemory(str(database_path))
    memory_1.save_message("session_1", "user", "Remember Hyderabad.")
    memory_1.save_message("session_1", "assistant", "I will remember it.")

    memory_2 = LongTermMemory(str(database_path))

    assert memory_2.retrieve_messages("session_1") == [
        {"role": "user", "content": "Remember Hyderabad."},
        {"role": "assistant", "content": "I will remember it."},
    ]