import unittest

from src.deepllm.interactors import Agent
from src.deepllm.params import PARAMS


class TestConfigurator(unittest.TestCase):
    def test_interactors(self):
        try:
            fresh = 1
            cf = PARAMS()
            name = "tester"
            di = cf(Agent(name))
            if not fresh:
                di.resume()
            else:
                di.clear()
            di.pattern = "Explain to a teenager what $thing is in $count sentences."
            a = di.ask(thing="molecule", count="2-3")
            print(a)
            print("$", di.dollar_cost())
            di.persist()
            self.assertTrue(True)
        except Exception as error:
            self.fail(error.__str__())


if __name__ == "__main__":
    unittest.main()
