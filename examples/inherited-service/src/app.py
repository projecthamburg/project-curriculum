"""Record reader. Legacy v1 wire format."""


def parse(raw):
    """Split a record line into fields.

    The v1 wire format is comma-separated with no escaping.
    """
    return raw.split(",")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return [parse(line.rstrip("\n")) for line in fh if line.strip()]


def active_only(records):
    """Records whose final field is the literal 'active'."""
    return [r for r in records if r and r[-1] == "active"]
