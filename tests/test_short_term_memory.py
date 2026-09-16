from src.memory.short_term import ShortTermMemory


def test_memory_stores_messages():

    memory = ShortTermMemory()

    memory.add_message(
        "session_1",
        "user",
        "I am evaluating Hyderabad.",
    )

    memory.add_message(
        "session_1",
        "assistant",
        "I can help analyze the opportunity.",
    )

    messages = memory.get_messages("session_1")

    assert len(messages) == 2

    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "I am evaluating Hyderabad."

    assert messages[1]["role"] == "assistant"


def test_memory_is_separated_by_session():

    memory = ShortTermMemory()

    memory.add_message(
        "session_1",
        "user",
        "Message from session 1",
    )

    memory.add_message(
        "session_2",
        "user",
        "Message from session 2",
    )

    session_1 = memory.get_messages("session_1")
    session_2 = memory.get_messages("session_2")

    assert len(session_1) == 1
    assert len(session_2) == 1

    assert session_1[0]["content"] == "Message from session 1"
    assert session_2[0]["content"] == "Message from session 2"


def test_memory_clear():

    memory = ShortTermMemory()

    memory.add_message(
        "session_1",
        "user",
        "Temporary message",
    )

    memory.clear("session_1")

    assert memory.get_messages("session_1") == []