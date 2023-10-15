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


def from_md(table: str, header=None):
    """

    Args:
        table (str): a markdown table
        header (list, optional): a header of the columns

    Returns:
        pd.DataFrame
    """
    rows = []
    for line in table.split("\n"):
        extracted, is_header = _extract_line(line.strip(), len(rows) == 1)
        if is_header:
            if header is None:
                header = rows[0]
            rows.pop(0)
            continue

        if extracted == []:
            continue

        rows.append(extracted)

    return pd.DataFrame(rows, columns=header)
