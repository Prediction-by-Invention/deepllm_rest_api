import unittest

from src.deepllm.prompters import causal_prompter, sci_prompter
from src.deepllm.refiners import AbstractMaker, Advisor, Rater


class TestParams(unittest.TestCase):
    @unittest.skip("Needs reviewing!")
    def test_rater(self):
        try:
            prompter = causal_prompter
            goal = "The Fermi paradox"
            threshold = 0.60
            lim = 1

            r = Rater(initiator=goal, prompter=prompter, threshold=threshold, lim=lim)

            for a in r.solve():
                print("\nTRACE:")
                for x in a:
                    print(x)
                print()
            print("MODEL:", len(r.logic_model))
            c = r.costs()
            print("COSTS in $:", c)
            self.assertTrue(True)
        except Exception as error:
            self.fail(error.__str__())

    @unittest.skip("Needs reviewing!")
    def test_advisor(self):
        try:
            prompter = sci_prompter
            goal = "Low power circuit design"
            lim = 1

            r = Advisor(initiator=goal, prompter=prompter, lim=lim)

            for a in r.solve():
                print("\nTRACE:")
                for x in a:
                    print(x)
                print()

            c = r.costs()
            print("COSTS in $:", c)
            self.assertTrue(True)
        except Exception as error:
            self.fail(error.__str__())

    def test_abstract_maker1(self):
        try:
            writer = AbstractMaker(
                topic="logic programming",
                keywords="; ".join(
                    [
                        "Knowledge representation",
                        "Knowledge representation formalism",
                        "Knowledge-based systems",
                        "Ontology engineering",
                        "Conceptual graphs",
                    ]
                ),
            )
            writer.agent.resume()
            ta = writer.run()
            print()
            print(ta)
            print()
            print(f"\nKeywords: {writer.keywords}")
            writer.agent.persist()
            print("Cost: $", writer.agent.dollar_cost())
            self.assertTrue(True)
        except Exception as error:
            self.fail(error.__str__())

    def test_abstract_maker2(self):
        try:
            writer = AbstractMaker(
                topic="Large language models",
                keywords="; ".join(
                    [
                        "Natural language processing",
                        "Language modeling",
                        "Dependency parsing",
                        "Named entity recognition",
                        "Sentiment analysis",
                        "Word embeddings",
                    ]
                ),
            )
            writer.agent.resume()
            ta = writer.run()
            print()
            print(ta)
            print()

            print(f"Keywords: {writer.keywords}")
            writer.agent.persist()
            print("Cost: $", writer.agent.dollar_cost())
            self.assertTrue(True)
        except Exception as error:
            self.fail(error.__str__())


if __name__ == "__main__":
    unittest.main()
