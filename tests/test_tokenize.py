"""Tests for code-aware lexical tokenization."""

import pytest

from rac.context.tokenize import code_tokens


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("getUserName(user_id)", ["get", "user", "name", "user", "id"]),
        ("snake_case_name", ["snake", "case", "name"]),
        ("HTTPServer", ["http", "server"]),
        ("parseHTTPResponse", ["parse", "http", "response"]),
        ("XMLHttpRequest", ["xml", "http", "request"]),
        ("HTTP", ["http"]),
        ("MAX_RETRY_COUNT", ["max", "retry", "count"]),
        ("__init__(self):", ["init", "self"]),
        ("user__name", ["user", "name"]),
        ("count = 42", ["count", "42"]),
        ("version2Value", ["version2", "value"]),
        ("sha256_hash", ["sha256", "hash"]),
        ("user user", ["user", "user"]),
        ("", []),
        (" \n\t ", []),
        ("()[]{},._+-", []),
    ],
)
def test_code_tokens(text, expected):
    assert code_tokens(text) == expected


def test_multiline_code():
    text = (
        "@staticmethod\n"
        "def getUserName(user_id: int):\n"
        "    return users[user_id].displayName\n"
    )

    assert code_tokens(text) == [
        "staticmethod",
        "def",
        "get",
        "user",
        "name",
        "user",
        "id",
        "int",
        "return",
        "users",
        "user",
        "id",
        "display",
        "name",
    ]


def test_incomplete_code():
    # Completion queries can end in the middle of a statement.
    assert code_tokens("result = client.getUser(") == [
        "result",
        "client",
        "get",
        "user",
    ]


def test_comments_and_strings_are_included():
    text = '# Load user profile\nlabel = "UserName"'

    assert code_tokens(text) == [
        "load",
        "user",
        "profile",
        "label",
        "user",
        "name",
    ]


def test_naming_styles_produce_matching_terms():
    expected = ["get", "user", "name"]

    for text in ("getUserName", "GetUserName", "get_user_name", "GET_USER_NAME"):
        assert code_tokens(text) == expected