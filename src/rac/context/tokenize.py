"""Code-aware lexical tokens for BM25."""

from __future__ import annotations

import re


def code_tokens(text: str) -> list[str]:
    """Split identifiers on snake_case and camelCase, lowercase, drop punctuation.

    Example:
        "getUserName(user_id)" -> ["get", "user", "name", "user", "id"]

    Uses ASCII letters and digits. Keeps adjacent digits with their word,
    preserves token order and repetitions, and includes words from comments
    and strings. These are retrieval terms, not model-token budget units.
    """
    # Separate acronyms from following words: HTTPServer -> HTTP Server.
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)

    # Separate camelCase boundaries: getUser -> get User.
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)

    # Underscores, whitespace, and punctuation act as separators.
    return re.findall(r"[a-z0-9]+", text.lower())