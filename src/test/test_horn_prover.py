import unittest

from src.deepllm.horn_prover import test_horn_prover


class TestConfigurator(unittest.TestCase):
    def test_interactors(self):
        try:
            test_horn_prover()
        except Exception as error:
            self.fail(error.__str__())


if __name__ == "__main__":
    unittest.main()
