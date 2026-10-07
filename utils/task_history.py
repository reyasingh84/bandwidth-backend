from collections.abc import Mapping


HISTORY_ITEM_SEPARATOR = "*"
HISTORY_ENTRY_SEPARATOR = "#"


def _safe_visible_text(visible_text: str) -> str:
    return (
        visible_text.replace(HISTORY_ITEM_SEPARATOR, " ")
        .replace(HISTORY_ENTRY_SEPARATOR, " ")
    )


def append_history(history: str, visible_text: str, timestamp: int) -> str:
    entry = f"{_safe_visible_text(visible_text)}{HISTORY_ITEM_SEPARATOR}{timestamp}"
    return f"{history}{HISTORY_ENTRY_SEPARATOR if history else ''}{entry}"


def decode_history(history: str) -> dict[str, dict[str, int | str]]:
    if not history:
        return {}

    decoded: dict[str, dict[str, int | str]] = {}
    for sequence, entry in enumerate(history.split(HISTORY_ENTRY_SEPARATOR), start=1):
        visible_text, separator, timestamp_text = entry.rpartition(
            HISTORY_ITEM_SEPARATOR
        )
        if not separator or not visible_text or not timestamp_text.isdigit():
            continue

        decoded[str(sequence)] = {
            "visible": visible_text,
            "timestamp": int(timestamp_text),
        }
    return decoded


def decode_task_history(task: object) -> object:
    history = getattr(task, "history", None)
    if isinstance(history, str):
        task.history = decode_history(history)
    return task


def decode_tasks_history(tasks: list[object]) -> list[object]:
    return [decode_task_history(task) for task in tasks]
