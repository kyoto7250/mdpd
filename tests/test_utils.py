import unittest

import pandas as pd

from mdpd import utils


class TestUtils(unittest.TestCase):
    def test_from_md(self):
        df = utils.from_md(
            """
            | Syntax    | Description |
            | --------- | ----------- |
            | Header    | Title       |
            | Paragraph | Text        |
            """
        )
        assert (df == pd.read_csv("tests/fixtures/pattern_1.csv")).all().all()
