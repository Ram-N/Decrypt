from nltk.corpus import wordnet as wn
import sys
from nltk.tokenize import word_tokenize, sent_tokenize
import itertools


from utils import *


def find_ngrams(input_list, n):
    '''
    Given a list and N, generate all N grams
    Borrowed http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
    '''
    return zip(*[input_list[i:] for i in range(n)])


def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]


def containsAll(str,set):
    """ check whether seq str contains ALL of the items in set. """
    print(str,set)
    if str:
        return 0 not in [c in str for c in set]

    return 0 #default is a No
#a trick from the Python Cookbook. Looking for whether '0' appears in the condition c in str for c in set


def getMeaningsList(oneword):
    """ store the meaning in a list """
    wordDefinitionsList = []

    for word_meaning in wn.synsets(oneword):
        #return(word_meaning.definition.split())
        wordDefinitionsList.append(word_meaning.definition)
        
    return wordDefinitionsList


def getBagOfWords(listOfMeanings):
    """Takes a list of sentences (meanings) and returns just a list of words"""

    return [w for m in listOfMeanings for w in m.split()]

def getBagOfWordsOfLenN(word, N):
    """Given a word, get its WordNet meanings and return just a list of words of Len N"""
    
    meaningsList = getMeaningsList(word)
    return [w for m in meaningsList for w in m.split() if (w.__len__() == N)] 


def getWordMeaningOfLenN(word,N):
    '''
    Looks at the English dictionary for synonyms of X of word-length N.
    '''
    mw = meaningList(word)
    dList = []
    synList = [w for w in mw if (w.__len__() == N)] # all the N-length (possible) synonyms

    # check for the other direction. Does X appear in n's meaning?
    for syn in synList:
        print("Trying to see if meaning of:",syn, "contains", word)
        s = set(meaning(syn))
        print s
        if set(word).issubset(s):
            dList.append(n)

    return dList


def areWordsSynonyms(word1, word2):
    '''
    returns 1 if the two words synonyms
    For the logic, we get the bagofMeaningWords for Word1, and for Word2
    We then see if these words are present in the other bag.
    '''

    set1 = set(getBagOfWords(getMeaningsList(word1)))
    set2 = set(getBagOfWords(getMeaningsList(word2)))

    if word2 in set1:
        print("Match of", word2, "with set of", set1)

    if word1 in set2:
        print("Match 1-2 of", word1, "with set of", word2, set2)
    


#idrisr github functions
#very useful library of defs

# Contains common utility functions used to solve NPR word puzzles

def sort_word(word):
    """sorts word and removes white spaces"""
    l = [letter for letter in word]
    l.sort(reverse=False)
    sort_word = ''.join([letter for letter in l])
    return sort_word

def swap_letter(s, letter, index):
    """takes a string 's' and replaces s['index'] with 'letter"""
    s = s[:index] + letter + s[index+1:]
    return s

def has_string(big_word, small_word):
    """returns boolean of whether small_word contained in big_word"""
    return -1<>big_word.find(small_word)

def is_len(_iter, length):
    """return boolean of whether '_iter' is lenght of 'length'"""
    return len(_iter)==length

def permutate(seq):
    """permutate a sequence and return a list of the permutations"""

    # To Do: create another version which only returns perms that are in dictioary

    # To Do: Change to return a unique list of perms
    if not seq:
        return [seq]  # is an empty sequence
    else:
        temp = []
        for k in range(len(seq)):
            part = seq[:k] + seq[k+1:]
            for m in permutate(part):
                x=seq[k:k+1] + m
                temp.append(x)
        return temp

def load_word_dictionary(path='/home/idris/work/npr_puzzles/word_lists/CROSSWD.TXT'):
    """takes "path" that is path of word list file. Function assumes one word per line.
    White space and capitalization stripped out.  returns dictionary of words with key=word, and value=None"""
    f = open(path, 'r')
    d= dict()
    for line in f.readlines():
        d[line.strip().lower()] = None
    return d

def check_synonym(word, word2):
    """checks to see if word2 is a synonym of word2"""
    l_syns = list()
    synsets = wn.synsets(word)
    for synset in synsets:
        if word2 in synset.lemma_names:
            l_syns.append( (word, word2) )
    return l_syns

def ends_with_letter(word, letter):
    """takes "word" and tests to see if last letter is 'letter'"""
    if len(word)>0:
        return word[-1] == letter
    else:
        return False

def split_word_once(word, min_char=2):
    """takes a word and splits it into two segments, with at least 'min_char' in
    each segment. Stores segment in a list, and ultimately returns a list of the
    segment lists"""
    l_segments = list()
    for split in range(min_char, len(word) - min_char + 1):
        l_segment = list()
        l_segment.append( word[:split] )
        l_segment.append( word[split:] )
        l_segments.append( l_segment ) 

    return l_segments

def word_in_dict(word, d):
    return word in d


def get_synonyms(word):
#TODO: return a list of them
#TODO: return list of a certain word length    
    syn_sets = wn.synsets(word)
    for syn_set in syn_sets:
        print '%s synonyms:\t%s' % (syn_set, syn_set.lemma_names)


def get_synonyms_of_length_N(word, N):
#TODO: return a list of them
#TODO: return list of a certain word length    
    syns = []
    word = word.lower()
    syn_sets = wn.synsets(word)
    for syn_set in syn_sets:
        for l in syn_set.lemma_names:
            if len(l)==N and (l != word):
                print l, word
                syns.append(l)
                
    return syns


if __name__ == '__main__':


    word1 = "space"
    word2 = "void"
    
    meaningsList = getMeaningsList(word1)
    print_list(meaningsList)
    print("Meanings of ", word2)
    print_list(getMeaningsList(word2))


    bag = getBagOfWordsOfLenN(word2, 4)
    print_list(set(bag))
    bag = getBagOfWordsOfLenN(word2, 6)
    print_list(set(bag))

    areWordsSynonyms(word1, word2)

    #    text = '''It is a blue, small, and extraordinary ball. Like no other'''
    #    tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]


    
    sys.exit(0)
    getWordMeaningOfLenN("gather", 7)
    print meaningsList

