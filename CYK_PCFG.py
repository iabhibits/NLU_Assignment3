import nltk
from nltk import *
from nltk.corpus import treebank
from nltk import Nonterminal
from nltk.treetransforms import *
from nltk import treetransforms
from nltk.parse import pchart
import pickle
from nltk.tree import Tree, ProbabilisticTree
from functools import reduce
from pcfg import pcfg

class Parser():
    def __init__(self, grammar):
        self.grammar = grammar
        self.unk = '<UNK>'

    def parse(self, tokens):
        try:
            self.grammar.check_coverage(tokens)
        except ValueError as v:
            # print('Words not Found', v)
            words = v.args[0].split(':')[1].replace('"', '').replace("'", "")[:-1]
            for word in words.split(','):
                w = word.strip()
                if w in tokens:
                    idx = tokens.index(w)
                    tokens[idx] = self.unk

        parse_table = {}

        for index in range(len(tokens)):
            token = tokens[index]
            parse_table[index, index + 1, token] = token

        for length in range(1, len(tokens) + 1):
            for start in range(len(tokens) - length + 1):
                span = (start, start + length)

                changed = True
                while changed:
                    changed = False

                    span_coverage = []
                    
                    for production in self.grammar.productions():
                        matching_rules = self.SearchRules(production.rhs(), span, parse_table)

                        for matching_rule in matching_rules:
                            span_coverage.append((production, matching_rule))

                    for (production, children) in span_coverage:
                        subtrees = [c for c in children if isinstance(c, Tree)]
                        p = reduce(lambda pr, t: pr * t.prob(), subtrees, production.prob())
                        node = production.lhs().symbol()
                        tree = ProbabilisticTree(node, children, prob=p)

                        c = parse_table.get((span[0], span[1], production.lhs()))
                        
                        if c is None or c.prob() < tree.prob():
                            parse_table[span[0], span[1], production.lhs()] = tree
                            changed = True

        tree = parse_table.get((0, len(tokens), self.grammar.start()))
       

        return tree

    def SearchRules(self, rhs, span, parse_table):
        (start, end) = span

        if start >= end and rhs == ():
            return [[]]
        if start >= end or rhs == ():
            return []

        matching_rules = []
        for split in range(start, end + 1):
            l = parse_table.get((start, split, rhs[0]))
            if l is not None:
                rights = self.SearchRules(rhs[1:], (split, end), parse_table)
                matching_rules += [[l] + r for r in rights]

        return matching_rules

"""if __name__ == '__main__':
    treebank_download()
    try:
        with open('grammar.pkl', 'rb') as input_file:
            grammar = pickle.load(input_file)
    except FileNotFoundError as NF:
        train_idx = (len(treebank.fileids()) * 3 ) // 4
        test_idx = (len(treebank.fileids()) * 1 ) // 4
        grammar = pcfg(x_train)"""
    