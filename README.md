# E1-246(NLU) 2019: Assignment3
Implement PCFG and CYK parser using NLTK Penn Treebank

**Requirements:**
    
    NLTK
    Download Penn treebank:
    
        import nltk
        nltk.download('treebank')
        
    PYEVALB

**Usage**
    
    To train model for generating PCFG.
    python evaluate.py train        
    
    To evaluate trained model on test dataset ( 10% of penn treebank )
    python evaluate.py evaluate
    
    To evaluate the model using the custom sentence.
    python evaluate.py test 'your_sentence'  
    
