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
