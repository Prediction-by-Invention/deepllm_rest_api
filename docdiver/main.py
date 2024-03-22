from time import time
from collections import Counter
import networkx as nx
from sentence_store.main import Embedder
from sentify.main import sentify
from deepllm.api import *


SENT_CACHE = './SENT_CACHE/'
SENT_STORE_CACHE = './SENT_STORE_CACHE/'

def as_local_file_name(doc_type, doc_name, saved_file_name):
    if not saved_file_name:
        if doc_type == 'url':
            file_name = doc_name.split('/')[-1]
        elif doc_type == 'wikipage':
            file_name = doc_name.replace(' ', '_') + ".txt"
        else:
            file_name = doc_name
    else:
        file_name = saved_file_name

    file_name = file_name.replace('.pdf', '.txt').replace('.PDF', '.txt')
    return file_name


class SourceDoc:
    def __init__(self, doc_type=None, doc_name=None, saved_file_name=None, threshold=None, top_k=None, trace=False):
        args = (doc_type, doc_name, threshold, top_k)
        assert None not in args, args
        self.doc_type = doc_type
        self.doc_name = doc_name
        self.threshold = threshold
        assert top_k > 0, top_k
        self.top_k = top_k
        self.trace = trace
        self.costs = 0
        self.times = Counter()

        self.saved_file_name = as_local_file_name(
            self.doc_type,
            self.doc_name,
            saved_file_name
        )

        sents, t_convert, t_segment = sentify(
            doc_type,
            doc_name,
            store=SENT_CACHE + self.saved_file_name,
            return_timings=True
        )

        self.emb = Embedder(doc_name)
        self.emb.store(sents)
        self.times['sentify_conversion'] = t_convert
        self.times['sentify_segmentation'] = t_segment

    def get_sents(self):
        res = self.emb.get_sents()
        return res

    def get_knns(self):
        res = self.emb.knns(self.top_k,as_weights=True)
        return res

    def extract_summary(self, best_k=10):
        knns = self.get_knns()
        g = nx.DiGraph()
        t1 = time()
        for i, ns in enumerate(knns):
            for (n, r) in ns:
                g.add_edge(i, n, weight=r)
        ranked = nx.pagerank(g)
        ranked = sorted(ranked.items(), key=lambda x: x[1], reverse=True)
        ranked = ranked[0:best_k]
        best_ids = sorted(i for (i, _) in ranked)
        sents = self.get_sents()
        res = [(i, sents[i]) for i in best_ids]
        t2 = time()
        self.times['extract_summary'] += t2 - t1
        print('SALIENT SENTENCES:', len(res), 'out of:', len(sents))
        return res

    def summarize(self, best_k=8, mark=1):
        def emphasize(w, important):
            if w.lower() not in important: return w
            return f":green[{w}]"

        id_sents = self.extract_summary(best_k=best_k)

        if self.trace:
            for x in id_sents:
                print(x)
            print()
        sents = [s for (_, s) in id_sents]

        text = " ".join(sents)
        sm = SummaryMaker(text, sum_size=best_k, kwd_count=8)
        text = sm.run()
        self.costs += sm.dollar_cost()
        self.times['llm_summary_maker_agent'] += sm.agent.processing_time
        source_words = set(w.lower() for s in sents for w in s.split())
        target_words = text.split()
        if mark:
            target_words = [emphasize(w, source_words) for w in target_words]
            text = " ".join(target_words)
            # text = text.replace(' .', '. ').replace(' ?', '? ')
            text = text.replace('Keyphrases:', '\n\nKeyphrases:')
        if text.startswith('Summary'): return text
        return 'Summary: ' + text

    def review(self, best_k=200):
        id_sents = self.extract_summary(best_k)

        if self.trace:
            for x in id_sents:
                print(x)
            print()
        sents = [s for (_, s) in id_sents]
        text = " ".join(sents)
        pr = PaperReviewer(text)
        text = pr.run()
        self.costs += pr.dollar_cost()
        self.times['llm_reviewer_agent'] = pr.agent.processing_time
        return 'Review: ' + text

    def retrieve(self, query, top_k=None):
        if top_k is None: top_k = self.top_k

        sents_rs = self.emb.query(query, top_k)

        return [sent for (sent, r) in sents_rs]

    def ask(self, quest, top_k=20):
        t1 = time()
        sents = self.retrieve(quest, top_k=top_k)
        text = " ".join(sents)
        agent = RetrievalRefiner(text, quest, tname=self.saved_file_name)
        answer_plus = agent.run()
        answer, follow_up = answer_plus.split('==>')
        answer = answer.strip()
        follow_up = follow_up.strip().replace('Follow-up question:', '')
        self.costs += agent.dollar_cost()
        t2 = time()
        self.times['llm_query_agent'] += t2 - t1
        return answer, follow_up

    def get_times(self):
        return self.times | self.emb.get_times()

    def dollar_cost(self):
        #self.costs += self.emb.dollar_cost()
        return self.costs


def test_main1(doc='https://arxiv.org/pdf/2306.14077.pdf'):
    # smarter_model()
    cheaper_model()
    # local_model()
    sd = SourceDoc(doc_type='url', doc_name=doc, threshold=0.5, top_k=3)
    sents = sd.summarize(best_k=20)
    print(sents)


def test_main(

    doc='https://arxiv.org/pdf/2306.14077.pdf',
    quest='How is Horn Clause logic used to refine interaction with LLM dialog threads?'
):
    clear_caches()
    remove_dir(SENT_CACHE)

    print("DOC:", doc)
    print('QUEST:', quest)
    # smarter_model()
    cheaper_model()
    # local_model()
    sd = SourceDoc(doc_type='url', doc_name=doc, threshold=0.5, top_k=3)
    sents = sd.retrieve(quest, top_k=20)
    print('RELEVANT SENTENCES:\n', len(sents))
    for s in sents:
        print(s)
    print('-' * 20, '\n')
    answer, follow_up = sd.ask(quest, top_k=20)
    print('ANSWER:\n', answer)
    print()
    print('FOLLOW_UP QUESTION:\n', follow_up)
    print()
    print("COSTS: $", round(sd.dollar_cost(), 4))
    print("TIMES:")
    for k, v in sd.get_times().items():
        print(k, '=', v)


if __name__ == "__main__":
    test_main()
