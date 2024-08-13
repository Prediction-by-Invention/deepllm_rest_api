import unittest

from src.deepllm.prompters import sci_prompter
from src.deepllm.recursors import run_explorer


class TestRecursors(unittest.TestCase):
    @unittest.skip("Needs reviewing!")
    def test_interactors(self) -> None:
        try:
            run_explorer(prompter=sci_prompter, goal="Logic programming", lim=1)
        except Exception as error:
            self.fail(error.__str__())


if __name__ == "__main__":
    unittest.main()
