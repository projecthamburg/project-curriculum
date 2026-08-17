"""Record writer."""

DELIM = ","
QUOTE = '"'


def format_field(value):
    """Quote a field when it contains the delimiter, so the row stays unambiguous."""
    if DELIM in value:
        return f"{QUOTE}{value}{QUOTE}"
    return value


def format_record(fields):
    return DELIM.join(format_field(f) for f in fields)


def dump(records, path):
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(format_record(r) + "\n")
