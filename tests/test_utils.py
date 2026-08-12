import unittest

import pandas as pd

from mdpd import utils


class TestUtils(unittest.TestCase):
    def test_simple_pattern_from_md(self):
        df = utils.from_md(
            """
            | Syntax    | Description |
            | --------- | ----------- |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/simple_pattern.csv")).all().all()

        df = utils.from_md(
            """
            +------------+-------------+
            | Syntax     | Description |
            +------------+-------------+
            | Header     | Title       |
            | Paragraph  | Text        |
            +------------+-------------+
            """
        )
        assert (df == pd.read_csv("tests/fixtures/simple_pattern.csv")).all().all()

        df = utils.from_md(
            """
            | Syntax    | Description |
            | :-------- | ----------: |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/simple_pattern.csv")).all().all()

    def test_header_only_from_md(self) -> None:
        df = utils.from_md(
            """
            | Syntax    | Description |
            | --------- | ----------- |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/header_only.csv")).all().all()

        df = utils.from_md(
            """
            +------------+-------------+
            | Syntax     | Description |
            +------------+-------------+
            """
        )
        assert (df == pd.read_csv("tests/fixtures/header_only.csv")).all().all()

        df = utils.from_md(
            """
            | Syntax    | Description |
            | :-------- | ----------: |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/header_only.csv")).all().all()

    def test_one_column_from_md(self):
        df = utils.from_md(
            """
            | Syntax    |
            | --------- |
            | Header    |
            | Paragraph |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/one_column.csv")).all().all()

        df = utils.from_md(
            """
            +------------+
            | Syntax     |
            +------------+
            | Header     |
            | Paragraph  |
            +------------+
            """
        )
        assert (df == pd.read_csv("tests/fixtures/one_column.csv")).all().all()

        df = utils.from_md(
            """
            | Syntax    |
            | :-------- |
            | Header    |
            | Paragraph |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/one_column.csv")).all().all()

    def test_one_column_header_only_from_md(self):
        df = utils.from_md(
            """
            | Syntax    |
            | --------- |
            """
        )
        assert (
            (df == pd.read_csv("tests/fixtures/one_column_header_only.csv")).all().all()
        )
        df = utils.from_md(
            """
            +------------+
            | Syntax     |
            +------------+
            """
        )
        assert (
            (df == pd.read_csv("tests/fixtures/one_column_header_only.csv")).all().all()
        )

        df = utils.from_md(
            """
            | Syntax    |
            | :-------- |
            """
        )
        assert (
            (df == pd.read_csv("tests/fixtures/one_column_header_only.csv")).all().all()
        )

    def test_no_header_from_md(self):
        df = utils.from_md(
            """
            | Syntax    | Description |
            """
        )
        assert (
            (df == pd.read_csv("tests/fixtures/header_only.csv", header=None))
            .all()
            .all()
        )

        df = utils.from_md(
            """
            | Syntax    | Description |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert (
            (df == pd.read_csv("tests/fixtures/simple_pattern.csv", header=None))
            .all()
            .all()
        )

        df = utils.from_md(
            """
            | Header    | Title       |
            | Paragraph | Text        |
            """,
            header=["Syntax", "Description"],
        )
        assert (df == pd.read_csv("tests/fixtures/simple_pattern.csv")).all().all()

    def test_with_header_from_md(self):
        df = utils.from_md(
            """
            | Column 1  | Column 2    |
            | --------- | ----------- |
            | Header    | Title       |
            | Paragraph | Text        |
            """,
            header=["Syntax", "Description"],
        )
        assert (df == pd.read_csv("tests/fixtures/simple_pattern.csv")).all().all()

    def test_convert_dtypes(self):
        df = utils.from_md(
            """
            |   GrossInternalArea | BuildingType                          | ConstructionDeliveryType   | BuildingName   |
            |--------------------:|:--------------------------------------|:---------------------------|:---------------|
            |                  10 | Office - General                      | newbuild                   | A              |
            |                  10 | Office - General                      | retrofit-in-one-go         | A              |
            |                  20 | Commercial Resi - Student Residential | newbuild                   | B              |
            |                  20 | Commercial Resi - Student Residential | retrofit-in-one-go         | B              |
            """,
            convert_dtypes=True,
        )
        assert pd.api.types.is_integer_dtype(df["GrossInternalArea"].dtype)

    def test_single_line_with_separator_from_md(self):
        """Single data row with a separator — the original bug scenario."""
        df = utils.from_md(
            """
            | Syntax    | Description |
            | --------- | ----------- |
            | Header    | Title       |
            """
        )
        assert list(df.columns) == ["Syntax", "Description"]
        assert len(df) == 1
        assert df.iloc[0]["Syntax"] == "Header"
        assert df.iloc[0]["Description"] == "Title"

    def test_single_line_with_provided_header_from_md(self):
        """Single data row, no separator, header provided explicitly — should not treat row as separator."""
        df = utils.from_md(
            """
            | Header    | Title       |
            """,
            header=["Syntax", "Description"],
        )
        assert list(df.columns) == ["Syntax", "Description"]
        assert len(df) == 1
        assert df.iloc[0]["Syntax"] == "Header"
        assert df.iloc[0]["Description"] == "Title"

    def test_single_line_with_separator_and_provided_header_from_md(self):
        """Single data row with separator AND pre-supplied header — separator should be skipped."""
        df = utils.from_md(
            """
            | Column 1  | Column 2 |
            | --------- | -------- |
            | foo       | bar      |
            """,
            header=["Syntax", "Description"],
        )
        assert list(df.columns) == ["Syntax", "Description"]
        assert len(df) == 1
        assert df.iloc[0]["Syntax"] == "foo"
        assert df.iloc[0]["Description"] == "bar"

    def test_single_column_single_line_from_md(self):
        """Single column, single data row — edge case for the fix."""
        df = utils.from_md(
            """
            | Syntax    |
            | --------- |
            | Header    |
            """
        )
        assert list(df.columns) == ["Syntax"]
        assert len(df) == 1
        assert df.iloc[0]["Syntax"] == "Header"

    def test_single_line_no_separator_from_md(self):
        """Single data row without a separator row and no pre-supplied header."""
        df = utils.from_md(
            """
            | Header    | Title       |
            """
        )
        # No separator -> treated as headerless, one row of data
        assert len(df) == 1
        assert list(df.iloc[0]) == ["Header", "Title"]
