#!/usr/bin/env python3
"""governance/redact_util.py — shared secret-pattern redaction.

Used by every capture path before anything reaches disk. Redaction happens in memory:
matched values are NEVER printed, only pattern labels and counts. Verify a flagged match
by its length and structural shape, never by printing the matched content.

This is a backstop, not the whole control. It cannot catch a credential shape it has no
pattern for, which is why protocol/ICE.md requires a deliberate sweep of any capture
before it lands in a tracked folder rather than trusting this module alone.
"""
from __future__ import annotations
import re

REDACTION_PATTERNS = [
    ("AWS access key ID",
     re.compile(r"AKIA[A-Z0-9]{16}"),
     "[REDACTED-AWS-ACCESS-KEY-ID]"),
    ("AWS secret access key assignment",
     re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{35,45}['\"]?"),
     "AWS_SECRET_ACCESS_KEY=[REDACTED-AWS-SECRET]"),
    # Project-scoped keys carry extra hyphens (the sk-proj-... shape), so the suffix class
    # must not be alphanumeric-only.
    ("OpenAI-style key",
     re.compile(r"(?<![A-Za-z0-9])sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
     "[REDACTED-OPENAI-KEY]"),
    ("Anthropic-style key",
     re.compile(r"(?<![A-Za-z0-9])sk-ant-[A-Za-z0-9_-]{20,}"),
     "[REDACTED-ANTHROPIC-KEY]"),
    ("GitHub token",
     re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
     "[REDACTED-GITHUB-TOKEN]"),
    ("Google API key",
     re.compile(r"AIza[A-Za-z0-9_\-]{20,}"),
     "[REDACTED-GOOGLE-API-KEY]"),
    ("Google OAuth2 access token",
     re.compile(r"ya29\.[A-Za-z0-9_\-]{20,}"),
     "[REDACTED-GOOGLE-OAUTH2-TOKEN]"),
    ("Slack token",
     re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
     "[REDACTED-SLACK-TOKEN]"),
    ("Generic api_key= assignment",
     re.compile(r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
     "[REDACTED-API-KEY-ASSIGNMENT]"),
    ("Generic secret= assignment",
     re.compile(r"secret\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
     "[REDACTED-SECRET-ASSIGNMENT]"),
    ("Generic token= assignment",
     re.compile(r"token\s*[:=]\s*['\"][A-Za-z0-9_\-]{20,}['\"]"),
     "[REDACTED-TOKEN-ASSIGNMENT]"),
    ("Bearer token",
     re.compile(r"Bearer\s+[A-Za-z0-9\-_.]{20,}"),
     "Bearer [REDACTED-TOKEN]"),
    ("PEM private key block",
     re.compile(r"-----BEGIN[ A-Z]*PRIVATE KEY-----[\s\S]*?-----END[ A-Z]*PRIVATE KEY-----"),
     "[REDACTED-PEM-PRIVATE-KEY-BLOCK]"),
]


def redact(text: str) -> tuple[str, dict]:
    """Return (redacted_text, {pattern_label: count}). Counts only — never the values."""
    counts: dict = {}
    for label, pattern, placeholder in REDACTION_PATTERNS:
        text, n = pattern.subn(placeholder, text)
        if n:
            counts[label] = counts.get(label, 0) + n
    return text, counts


def scan_only(text: str) -> dict:
    """Non-destructive: report {pattern_label: count} without rewriting anything."""
    return {label: len(pattern.findall(text))
            for label, pattern, _ in REDACTION_PATTERNS
            if pattern.search(text)}
