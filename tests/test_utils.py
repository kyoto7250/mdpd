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
