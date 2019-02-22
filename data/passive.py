import nltk
import sys
import os
from itertools import dropwhile
import postagger
import numpy as np



def tag_sentence(sent):
    """Take a sentence as a string and return a list of (word, tag) tuples."""
    assert isinstance(sent, basestring)

    tokens = nltk.word_tokenize(sent)
    return postagger.get_tagger().tag(tokens)

def passivep(tags):
    """Takes a list of tags, returns true if we think this is a passive
    sentence."""
    # Particularly, if we see a "BE" verb followed by some other, non-BE
    # verb, except for a gerund, we deem the sentence to be passive.
    
    postToBe = list(dropwhile(lambda(tag): not tag.startswith("BE"), tags))
    nongerund = lambda(tag): tag.startswith("V") and not tag.startswith("VBG")

    filtered = filter(nongerund, postToBe)
    out = any(filtered)

    return out

def oneline(sent):
    """Replace CRs and LFs with spaces."""
    return sent.replace("\n", " ").replace("\r", " ")


def decide_if_active(sent):
    """Given a sentence, tag it and print if we think it's a passive-voice
    formation."""
    isactive = np.nan

    tagged = tag_sentence(sent)
    tags = map( lambda(tup): tup[1], tagged)

    if passivep(tags):
        print "passive:", oneline(sent)
        isactive = 0;
    else:
    	isactive = 1;
    return isactive
