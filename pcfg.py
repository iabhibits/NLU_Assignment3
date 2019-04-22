import nltk
from nltk import *
from nltk.corpus import treebank
from nltk import Nonterminal
from nltk.treetransforms import *
from nltk import treetransforms
import pickle

# Download Penn Treebank using NLTK interface

def treebank_download():
    nltk.download('treebank')
    return

# Calculate Probabilities of production rules

def learn_pcfg(start, productions):
	"""
	parameter--->
	:start = S | Root non-terminal symbol
	:production = CFG Production rules | list of CFG production rules

	Return --->
	:start = S | Root non-terminal symbol
	:production = PCFG Production rules | list of PCFG production rules
	____________________________________________________________________

	Probabilities are calculated using relative frequency estimation:
	The probability of a production X -> a in a PCFG is:

    |                count(X -> a)
    |  P(X -> a) = ---------------       
    |                 count(X)
    _____________________________________________________________________

	"""
	pcount = {}
	lcount = {}
    
	for prod in productions:
	    lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1
	    pcount[prod] = pcount.get(prod,0) + 1
	    
	prods = [ProbabilisticProduction(p.lhs(), p.rhs(), prob=pcount[p] / lcount[p.lhs()]) for p in pcount]
	with open('grammar.pcfg', 'w') as f:
		for item in prods:
			f.write("%s\n" % item)
	return PCFG(start, prods)

def smoothing_pcfg(words, grammar, smoothing=None):
    pcount = {}
    lcount = 0
    new_prods = []
    lhs = None
    for prod in grammar.productions():
        if str(prod.lhs()) == 'NN':
            lhs = prod.lhs()
            lcount += 1
            pcount[prod] = pcount.get(prod, 0) + 1

    add = len(words) + len(pcount)
    avg = 1 / lcount

    if lhs is None:
        lhs = Nonterminal('NN')

    for word in words:
        rhs = (word.strip("'"), )
        if smoothing is None:
            prob = 1 / (lcount + add)
        else:
            prob = avg / len(words)
        prod = ProbabilisticProduction(lhs, rhs, prob=prob)
        new_prods.append(prod)

    for p in grammar.productions():
        if str(p.lhs()) == 'NN':
            if smoothing is None:
                p = ProbabilisticProduction(p.lhs(), p.rhs(), prob= (pcount[p] + 1) / (lcount + add))
            else:
                p = ProbabilisticProduction(p.lhs(), p.rhs(), prob= p.prob() - (avg / lcount))
        new_prods.append(p)
    return PCFG(grammar.start(), new_prods)


def smoothing_pcfg_new(start, productions):
	"""
	parameter--->
	:start = S | Root non-terminal symbol
	:production = CFG Production rules | list of CFG production rules

	Return --->
	:start = S | Root non-terminal symbol
	:production = PCFG Production rules | list of PCFG production rules
	____________________________________________________________________

	Probabilities are calculated using relative frequency estimation:
	The probability of a production X -> a in a PCFG is:

    |                count(X -> a)
    |  P(X -> a) = ---------------       
    |                 count(X)
    _____________________________________________________________________

	"""
	pcount = {}
	lcount = {}
	cnt = 0
    
	for prod in productions:
	    lcount[prod.lhs()] = lcount.get(prod.lhs(), 0) + 1
	    pcount[prod] = pcount.get(prod,0) + 1
	    cnt += 1
	    
	prods = [ProbabilisticProduction(p.lhs(), p.rhs(), prob=(pcount[p] + 1 ) / (lcount[p.lhs()] + cnt )) for p in pcount]
	with open('grammar_smooth.pcfg', 'w') as f:
		for item in prods:
			f.write("%s\n" % item)
	return PCFG(start, prods)

def pcfg(train_idx = None,smoothing = None):
	"""
    productions = []
    item = treebank._fileids[0]
    print("ITEM\n\n",item,"\n\n")
    for tree in treebank.parsed_sents(item)[:3]:
        # perform optional tree transformations, e.g.:
        tree.collapse_unary(collapsePOS = False)
        tree.chomsky_normal_form(horzMarkov = 2)
        productions += tree.productions()
"""	
	if train_idx == None:
		train_idx = (len(treebank.fileids()) * 3 ) // 4
	productions = []
	for item in treebank.fileids()[0:train_idx]:
	    for tree in treebank.parsed_sents(item):
	        tree.collapse_unary(collapsePOS = False)# Remove unary production rule
	        tree.chomsky_normal_form(horzMarkov = 2)# Convert into chomsky normal form i.e., A->(B,C,D) into A->(B,E) E->(C,D)
	        productions += tree.productions()

	S = Nonterminal('S')
	if smoothing == None:
		grammar = learn_pcfg(S, productions)
	elif smoothing == 'L1':
		grammar = smoothing_pcfg(S,productions)

	with open('grammar.pkl', 'wb') as f:
		pickle.dump(grammar,f)

	return grammar


"""def cky_parser(sent, grammar):




print("Parse sentence using induced grammar:")

parser = pchart.InsideChartParser(grammar)
parser.trace(3)

# doesn't work as tokens are different:
#sent = treebank.tokenized('wsj_0001.mrg')[0]

sent = treebank.parsed_sents(item)[0].leaves()
print(sent)
for parse in parser.parse(sent):
    print(parse)
"""
	