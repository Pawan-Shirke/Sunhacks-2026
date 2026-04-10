"""
Diff Agent — compares old vs new regulation text using difflib.
"""
import difflib


def compute_diff(old_text: str, new_text: str, context: int = 3) -> str:
    """
    Return a unified diff string between old_text and new_text.
    Lines starting with '+' are additions, '-' are removals.
    """
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile="previous_version",
        tofile="new_version",
        n=context,
        lineterm=""
    )
    return "\n".join(diff)


def extract_changes(diff_text: str):
    """
    Parse a unified diff string into added and removed lines.
    Returns dict with 'added' and 'removed' lists.
    """
    added = []
    removed = []
    for line in diff_text.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:].strip())
        elif line.startswith("-") and not line.startswith("---"):
            removed.append(line[1:].strip())
    return {"added": added, "removed": removed}


def summarize_changes(diff_text: str) -> str:
    """
    Generate a human-readable bullet summary of changes.
    """
    changes = extract_changes(diff_text)
    lines = []
    for item in changes["added"]:
        if item:
            lines.append(f"+ {item}")
    for item in changes["removed"]:
        if item:
            lines.append(f"- {item}")
    return "\n".join(lines) if lines else "No textual changes detected."
