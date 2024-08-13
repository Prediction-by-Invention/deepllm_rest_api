import unittest

from src.deepllm.api import run_advisor, run_rater, run_recursor
from src.deepllm.params import jpp
from src.deepllm.prompters import conseq_prompter, sci_prompter, task_planning_prompter


class TestAPI(unittest.TestCase):
    @unittest.skip("Needs reviewing!")
    def test_api(self):
        try:
            for x in run_recursor(
                prompter=task_planning_prompter, initiator="Build a Chat Bot", lim=1
            ):
                jpp(x)
            for x in run_recursor(
                prompter=conseq_prompter,
                initiator="Emergence of superhuman artificial general intelligence",
                lim=1,
            ):
                jpp(x)
            for x in run_advisor(
                prompter=conseq_prompter, initiator="Practical fusion reactors", lim=1
            ):
                jpp(x)

            for x in run_rater(
                prompter=sci_prompter,
                initiator="Low power circuit design",
                threshold=0.95,
                lim=1,
            ):
                jpp(x)

            for x in run_rater(
                prompter=sci_prompter,
                initiator="Low power circuit design",
                threshold=0.50,
                lim=1,
            ):
                jpp(x)
            self.assertTrue(True)
        except Exception as error:
            self.fail(error.__str__())


if __name__ == "__main__":
    unittest.main()
