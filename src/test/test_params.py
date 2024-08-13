import unittest

from src.deepllm.params import PARAMS


class Temp:
    def __init__(self):
        self.hi = "hello"


class TestParams(unittest.TestCase):

    def test_params(self) -> None:
        cf = PARAMS()
        cf.TRACE = 1  # type: ignore
        d = cf(Temp())
        self.assertEqual(d.TRACE, 1)


if __name__ == "__main__":
    unittest.main()
