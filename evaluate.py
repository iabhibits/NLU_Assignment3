import nltk
from nltk import *
from nltk.corpus import treebank
from nltk import Nonterminal
from nltk.treetransforms import *
from nltk import treetransforms
from nltk.parse import pchart
from PYEVALB.scorer import Scorer
from PYEVALB import parser
import pickle
from CYK_PCFG import Parser
from pcfg import *
from CYK_PCFG import *



def test_pcfg(test_idx, grammar=None):
    if grammar == None:
    	print("No PCFG grammar found\n")
    	return
    p = Parser(grammar)
    goldtest = []
    for idx, x in enumerate(test_idx):
        for idx2, tree in enumerate(treebank.parsed_sents(x)):
            tree_words = list(map(lambda x: x.strip().replace('"', ''), tree.leaves()))
            print('Sentence:', tree_words)
            try:
                grammar.check_coverage(tree_words)
            except ValueError as v:
                
                new_words = set()
                words = v.args[0].split(':')[1].replace('"', '').replace("'", "")[:-1]
                for word in words.split(','):
                    new_words.add(word.strip())
                grammar = update_grammar(new_words, grammar)
                p = Parser(grammar)
            try:
                test_tree = p.parse(tree_words)
                if test_tree :
                    print(test_tree)
                    gold_test.append((str(tree), str(test_tree.pformat())))
                    evaluate([goldtest[-1]])
                else:
                    print('No tree')
            except ValueError as v:
                print('No tree. ', v)
            
    print('Got parse trees for: ', len(goldtest), 'sentences.')
    return goldtest

def evaluate(goldtest):
    scorer = Scorer()
    for gold, test in goldtest:
        goldtree = parser.create_from_bracket_string(gold)
        testtree = parser.create_from_bracket_string(test)
        result = scorer.score_trees(gold_tree, test_tree)
        print(result)

#%%
def test(sentences):
    for sentence in sentences:
        tokens = sentence.split()
        grammar = load_grammar()
        p = Parser(grammar)
        tree = p.parse(tokens)
        if tree is None:
            print('No Tree')
        else:
            print(tree)
    tree.pretty_print()


if __name__ == '__main__':
    treebank_download()
    try:
        with open('grammar.pkl', 'rb') as input_file:
            grammar = pickle.load(input_file)
    except FileNotFoundError as NF:
        train_idx = (len(treebank.fileids()) * 3 ) // 4
        test_idx = (len(treebank.fileids()) * 1 ) // 4
        grammar = pcfg(x_train)
    p = Parser(grammar)
    sent = treebank.parsed_sents('wsj_0180.mrg')[0].leaves()
    tree = p.parse(sent)
    print("Parsing for wsj_0180.mrg")
    print(tree)

    evaluate()