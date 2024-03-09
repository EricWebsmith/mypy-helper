import unittest

from mypy_helper.fix_ignore_without_code import fix_ignore_without_code
from tests.unittest_ext import compare_files


class TestFixIgnoreWithoutCode(unittest.TestCase):
    def test_consider_replacement(self) -> None:
        fix_ignore_without_code(
            "examples/simple_example", "examples/simple_example/errors.txt", ".fix_ignore_without_code.actual"
        )
        compare_files(
            "examples/simple_example/example.py.fix_ignore_without_code.expected",
            "examples/simple_example/example.py.fix_ignore_without_code.actual",
        )


if __name__ == "__main__":
    unittest.main()
