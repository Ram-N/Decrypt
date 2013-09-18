#import enchant
from nltk.corpus import wordnet

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


def meaning(oneword):
    """ store the meaning in a list """

    for word_meaning in wordnet.synsets(oneword):
        #return(word_meaning.definition.split())

    for s in wn.synsets(word):
        # add each def to a list and return
        print s.definition



def getWordMeaningOfLenN(word,N):
    '''
    Looks at the English dictionary for synonyms of X of word-length N.
    '''
    mw = meaning(word)
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


if __name__ == '__main__':

    meaningsList = getWordMeaningOfLenN("gather", 7)
    print meaningsList

