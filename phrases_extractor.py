#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Manas Ranjan Kar
# @Date:   2016-06-20
# @Email:  manas@jsm.email  
# @Github username: @manasRK
# @Last Modified by:   Manas Ranjan KAr
# @Last Modified time: 2016-06-20


import re
import nltk
from unidecode import unidecode

# Inspired from http://www.aclweb.org/anthology/C10-1065
grammar = r"""
    NP:   {<NNP>?<NNP>?}
"""

def generate_tree(text):
    text = text.replace('“', '"') #to preserve quotes in text, primarily news content
    text = text.replace('”', '"')
    text = text.replace('’', "'")
    text = unidecode(text)
    chunker = nltk.RegexpParser(grammar)
    tokenized_text = nltk.tokenize.word_tokenize(text)
    postoks = nltk.tag.pos_tag(tokenized_text)
    tree = chunker.parse(postoks)
    return tree


def leaves(text):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in generate_tree(text).subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()


def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40)
    return accepted


def get_terms(text):
    for leaf in leaves(text):
        term = [ w for w,t in leaf if acceptable_word(w) ]
        yield term

def get_phrases(text):
    """ Extract important keywords, returns a list"""
    text = text.replace('“', '"') #to preserve quotes in text, primarily news content
    text = text.replace('”', '"')
    text = text.replace('’', "'")
    text = unidecode(text)
    terms = get_terms(text)
    phrases = []
    for all_terms in terms:
        # strip whitespaces & extract core term
        phrase = re.sub('\s+', ' ', " ".join(all_terms)).strip()
        if len(phrase.split()) > 1:
            phrases.append(phrase)
        else:
            pass
    return phrases

if __name__ == '__main__':
    
    text = '''
Responding to BJP MP Subramanian Swamy’s attack on Arvind Subramanian, the Finance Minister Arun Jaitley said the government had full confidence in him and his advice was of great value.    
'''    
    terms = get_terms(text)
    
    for all_terms in terms:
        phrase = re.sub('\s+',' ', " ".join(all_terms)).strip()
        if len(phrase.split())>1:
            print phrase
        else:
            pass
    
    print get_phrases(text)
