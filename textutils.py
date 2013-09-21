from nltk.corpus import wordnet
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

    for word_meaning in wordnet.synsets(oneword):
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

