import enchant
from nltk.corpus import wordnet

def containsAll(str,set):
    """ check whether seq str contains ALL of the items in set. """
    print(str,set)
    if str:
        return 0 not in [c in str for c in set]

    return 0 #default is a No
#a trick from the Python Cookbook. Looking for whether '0' appears in the condition c in str for c in set


def meaning(oneword):
    """ store the meaning in a list """

    for word_meaning in wordnet.synsets(oneword):
        return(word_meaning.definition.split())


def getWordMeaningOfLenN(x,N):
    ''' Looks at the dictionary for synonyms of X of word-length N. '''
    mw = meaning(x)
    nList = []
    dList = []
    nList = [w for w in mw if (w.__len__() == N)]

    # check for the other direction. Does X appear in n's meaning?
    for n in nList:
        print("Trying:",n)
        if containsAll(meaning(n),x):
            dList.append(n)

    return dList


def wc(filename):
    """Returns the number of characters, words and lines in a file.

The result is a tuple of the form (#characters, #words, #lines)."""
    data = open(filename,'rb').read()
    return (len(data), len(data.split()), len(data.splitlines()))


