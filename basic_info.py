#!/usr/bin/python2

# Randy Armknecht
# 19 Feb 2014
#
# Playing around with the Natural Language Processing Toolkit (nltk)
# http://www.nltk.org/
#

from __future__ import division
import sys
import nltk
from nltk.corpus import cmudict
from pprint import pprint
from hyphen import Hyphenator as hy

DICT = cmudict.dict()
SYLLABLE_AVG = 1.66

# START - Implemented from http://www.slideshare.net/pbpimpale/natural-language-toolkit-nltk-basics
def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())

    unusual = text_vocab.difference(english_vocab)
    return sorted(unusual)

def problem_words(text):
    return sorted(set(w.lower() for w in text if not w.isalpha()))

def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)

def plot_word_freq(text):
    text_vocab = [w.lower() for w in text if w.isalpha()]
    fdist = nltk.FreqDist(text_vocab)
    fdist.plot()

def long_words(text,length=10):
    text_vocab = [w.lower() for w in text if w.isalpha()]
    return set([w for w in text_vocab if len(w) > length])

def topic_words(text,length=7,freq=7):
    text_vocab = [w.lower() for w in text if w.isalpha()]
    fdist = nltk.FreqDist(text_vocab)
    return sorted([w for w in set(text_vocab) if len(w) > length and fdist[w] > freq])

def vocab_size(text):
    return len(set(text))

def vocab_richness(text):
    return len(text) / vocab_size(text)

def word_context(text,word):
    return text.concordance(word)

# END - Implemented from http://www.slideshare.net/pbpimpale/natural-language-toolkit-nltk-basics

def get_raw(fname):
    data = ""
    with open(sys.argv[1]) as f:
        data = f.read()
    return data

def massage_raw(raw):
    modified = ''.join([character for character in raw if ord(character) < 128])
    sentences = nltk.sent_tokenize(modified)
    tokens = [] 
    for s in sentences:
        for t in nltk.word_tokenize(s):
            tokens.append(t)
    return (nltk.Text(tokens), sentences)

def nsyl(word):
    return len([i for i in DICT[word.lower()][0] if i[-1].isdigit()])
#    return [len(list(y for y in x if y[-1].isdigit())) for x in DICT[word.lower()]][0]

# http://stackoverflow.com/a/5615724 translated to python
def count_syllables(word):
    # Special Cases
    if word in ['ll', 'noye', 'shae']:
        return 1

    # Back to Our Regular Scheduled Programming
    vowels = ['a','e','i','o','u','y']
    curword = word
    syls = 0
    lastWasVowel = False

    for wc in curword:
        foundVowel = False
        for v in vowels:
            # Don't Count Diphthongs
            if v == wc and lastWasVowel:
                foundVowel = True
                lastWasVowel = True
                break;
            elif v == wc and not lastWasVowel:
                syls += 1
                foundVowel = True
                lastWasVowel = True
                break;

        # If Fully cycle and no vowel found, set lastWasVowel to False
        if not foundVowel:
            lastWasVowel = False

    # Remove es, it's usually silent
    if len(curword) > 2 and curword[-2:] == "es":
        syls -= 1
    elif len(curword) > 1 and curword[-1] == "e":
        syls -= 1

    return syls



def flesch_kincaid(text,sentences):
    syllables = []
    misses = []
    words = [word for word in text if (len(word) > 1) or (word.lower() in ['a', 'i'])]
 
    for word in words:
        try:
            ns = nsyl(word)
            syllables.append(ns)
        except KeyError:
            n = count_syllables(word.lower())
            if n == 0:
                misses.append(word.lower())
            else:
                syllables.append(n)

    word_count = len(words) - len(misses)
    sentence_count = len(sentences)
    syllable_count = sum(syllables)
    
    #m_dist =  nltk.FreqDist(misses)
    #for t in m_dist.keys():
    #    print m_dist[t], t, count_syllables(t)
    #for m in set(misses):
    #    print "%s %d" % (m, m_dist[m])
    
    words_sents = word_count / sentence_count
    syl_words = syllable_count / word_count

    if word_count > 0 and sentence_count > 0:
        results = {
            'words': word_count,
            'syllables': syllable_count,
            'missed_count': len(misses),
            'missed_pct': len(misses) / (word_count + len(misses)),
            'sentences': sentence_count,
            'grade_level': (0.39 * words_sents) + (11.8 * syl_words) - 15.59,
            'reading_ease': 206.835 - (1.015 * words_sents) - (84.6 * syl_words),
        }
    return results    

if __name__ == "__main__":
    if len(sys.argv) is not 2:
        print "Usage: %s <text_file>" % (sys.argv[0])
        sys.exit(0)

    (text,sentences) = massage_raw(get_raw(sys.argv[1]))

    pprint(flesch_kincaid(text,sentences))
