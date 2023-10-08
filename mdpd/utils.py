import re

import pandas as pd


def _is_header(extracted):
    """
    >>> _is_header(["---", "---"])
    True
    >>> _is_header([":---", "---:", ":---:"])
    True
    >>> _is_header([":---", "foo", "bar"])
    False
    >>> _is_header(["foo", "bar"])
    False
    """
    partial_pattern = r":*-+:*"
    return all(re.match(partial_pattern, ex) for ex in extracted)


def _extract_line(line: str, possible_separator):
    """
    >>> _extract_line("| foo | bar |", False)
    (['foo', 'bar'], False)
    >>> _extract_line("| foo | bar |", True)
    (['foo', 'bar'], False)
    >>> _extract_line("| --- | --- |", False)
    (['---', '---'], False)
    >>> _extract_line("| --- | --- |", True)
    ([], True)
    """
    # need to accept overlapping patterns.
    vertical_pattern = r"(?=(\|(.*?)\|))"
    plus_pattern = r"(?=(\+(.*?)\+))"
    extracted = [value.strip() for _, value in re.findall(vertical_pattern, line)]
    if possible_separator and not extracted:
        # check this pattern's separator, ex. +-----+----+
        extracted = [value.strip() for _, value in re.findall(plus_pattern, line)]

    if not extracted:
        return [], False

    if possible_separator and _is_header(extracted):
        return [], True

    return extracted, False


def from_md(table: str):
    exist_header = False
    rows = []
    for line in table.split("\n"):
        extracted, is_header = _extract_line(line.strip(), len(rows) == 1)
        if is_header:
            exist_header = True

        if extracted == []:
            continue

        rows.append(extracted)

    if exist_header:
        return pd.DataFrame(rows[1:], columns=rows[0])
    return pd.DataFrame(rows)
