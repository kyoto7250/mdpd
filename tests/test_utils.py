import unittest

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

        assert df == ""
