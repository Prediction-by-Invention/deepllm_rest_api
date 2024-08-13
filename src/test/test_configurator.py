import unittest

from src.deepllm.configurator import Mdict


class TestConfigurator(unittest.TestCase):
    def test_configurator(self) -> None:
        d = Mdict(**dict(a=1, b=2, c=3, d=4, e=5))
        md = Mdict(a=22, c=33)
        md.b = 0  # type: ignore
        print("prompters:", d)
        print("md:", md)
        print("prompters:", md(d))
        cfg = Mdict(TRACE=0)
        print(cfg, type(cfg))
        self.assertEqual(d.a, 22)  # type: ignore
        self.assertEqual(d.b, 0)  # type: ignore
        self.assertEqual(d.c, 33)  # type: ignore


if __name__ == "__main__":
    unittest.main()
