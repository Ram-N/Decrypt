import itertools
from nltk.corpus import wordnet

import textutils

import cfg # src file with globals


def append_list_entry(anawords_list, line):
    grind = line.lstrip().rstrip('\n')
    anawords_list.append(grind.lower())

def read_anagrinds(filename,anawords_list):
    """ read the file anagrinds.txt and store as a List """
    fo = open(filename, "r")
    for line in fo:
        if line.find("#") == 1: #skip comments
            continue
        append_list_entry(anawords_list, line)
    fo.close()


######################

def identify_anagram_fodder(cluewords):
    """ There might be several fodders. Find all of them and add to global fodderList """

    fodLen=0
    cfg.numFods = 0
    fWords = ""

    clueEnd = cfg.numWordsInClue-1
    #remove the last token (it contains the length of the solution)
    cluewords.pop()

    print("Anag Parameters: Starts at",cfg.anagrindIndex,  cfg.numAnagrindWords)

    for i in range(clueEnd):
        if (i >= cfg.anagrindIndex) and (i<cfg.anagrindIndex+cfg.numAnagrindWords):
            continue #skip. Encountered AnagrInd. Cannot be fodder

        for j in range(i,clueEnd):
            if (j >= cfg.anagrindIndex) and (j<cfg.anagrindIndex+cfg.numAnagrindWords):
                fodLen = 0
                fWords = ""
                break #skip. Encountered AnagrInd. Cannot be fodder

            w = cluewords[j]
            fodLen += w.__len__() #add word lengths
            fWords += w
            if fodLen == cfg.solLen:
                cfg.fodStart.append(i)
                cfg.fodEnd.append(j)
                cfg.numFods += 1
                cfg.fodList.append(fWords)
                print("Found one", cfg.solLen, w, fodLen)
            if fodLen >= cfg.solLen: #includes the exact len match case as well
                fodLen = 0
                fWords = ""
                break #done with j, move on to next i

    return(cfg.numFods)

def check_if_full_anagram(fullclue):
    """ Are any of the AnagrInds present in the clue? """

    cfg.clueWords = fullclue.lower().split()
    anagfound =0
    defn = 0
    cluewords = cfg.clueWords

# check if there is a one- or two-word ANAGRIND

    for index in range(len(cluewords)):
        wd = cluewords[index]
        dbl = ""
        if index < len(cluewords)-1 :
            dbl = wd + " " + cluewords[index+1] # 2 word combos
        if cfg.anagrinds.count(wd) > 0:
            cfg.solTextSeq = cfg.addLine(cfg.solTextSeq, wd.upper()+ " indicates that Solution is a " + str(cfg.solLen)+ "-letter Anagram")
            #print(wd.upper(), "indicates that Solution is a", cfg.solLen, "-letter Anagram")
            anagfound =1
            cfg.anagrindIndex = index #starts at 0
            cfg.numAnagrindWords = 1
            break

        if dbl and (cfg.anagrinds.count(dbl) > 0): #compound if ensure dbl is non-empty
            cfg.solTextSeq = cfg.addLine(cfg.solTextSeq, dbl.upper()+ " dbl indicates that Solution is a "+ str(cfg.solLen)+ "-letter Anagram")
            #print(dbl.upper(), " dbl indicates that Solution is a ", cfg.solLen, "-letter Anagram")
            anagfound =1
            cfg.anagrindIndex = index #index starts at 0
            cfg.numAnagrindWords = 2
            break

    if anagfound == 0:
        cfg.solTextSeq = cfg.addLine(cfg.solTextSeq, "Doesn't seem to be a pure anagram")
        return 0

    # At this point, we know it IS an anagram
    aGrindword = wd

    # old fodderIdx = identify_anagram_fodder(cluewords,aGrindword,cfg.anagrindIndex)
    numFod = identify_anagram_fodder(cfg.clueWords)

    if numFod == 0:
        print("Fodder not found")

    if numFod:
        identify_definition(numFod) #which part of the clue is definition

    return(anagfound)
## end of check if anagram ##


def identify_definition(numFod):
    """ assign the part of clue to be definition, based on Anag fodder """

    defWords = []
    defList = []
    #There are numFod number of fodders. Need a definition for each fodder.
    for f in range(numFod):
        defWords = []
        #Basically, every word that is NOT Fodder and NOT AnagrInd is Fodder
        for i,w in enumerate(cfg.clueWords):
            if i >= cfg.fodStart[f] and i<= cfg.fodEnd[f]:
                continue
            if (i >= cfg.anagrindIndex) and (i<cfg.anagrindIndex+cfg.numAnagrindWords):
                continue #skip. Encountered AnagrInd. Cannot be fodder                continue
            defWords.append(w)

        defList.append(defWords)
        print("Possible Definition:",defWords)
        cfg.solTextSeq = cfg.addLine(cfg.solTextSeq, "\n Possible definition: " + " ".join(defWords))

        anafound = make_anagram(f,defWords)



def    make_anagram(fodNum, defWords):
    """ take the letters in each fodder and see if a valid word can be anagrammed """

#cfg.fodder and cfg.defwords are now known
    f = cfg.fodList[fodNum]
    cfg.solTextSeq += "Trying anagrams " + f + "\n"

    #verify that fodder length and solLen match

    #generate all valid Anagrams - solCandidates gets populated here
    numAnafound = generate_valid_anagrams(f)

    # check if the meaning of words in fodList is one of the anagram words
    if numAnafound:
        does_meaning_match(defWords, cfg.solCandidates[fodNum])

#need something better below
    return numAnafound


def does_meaning_match(defWords, solCandidates):
    """ Take the meaning of solCands and see if there is a match with definition.
    then take the meaning of definition words and see if solCandidate words are in them.
    """

    for sWord in solCandidates:
        print ("Trying the meaning of candidate - ",sWord)
        solMeanWords = myutils.meaning(sWord)

        for dw in defWords:
            if len(dw) <=2 : continue
            if dw in cfg.stopwords: continue
            if dw in solMeanWords:
                cfg.solTextSeq += "Strong Match!! \n"+sWord.upper()+ " Matches Defintion "+dw+" \n"
                continue

            defMeanWords = myutils.meaning(dw).split()
            for m in defMeanWords:
                if len(m) <=2 : continue
                if m in cfg.stopwords: continue
                if m in solMeanWords:
                    cfg.solTextSeq += "Possible Solution Found "+m.upper()+ " Matches Defintion "+dw+" \n"
                    break





def generate_valid_anagrams(letters):
    """ Using itertools to generate Anagrams. THen check against English dictionary"""

    solRow = []
    #each fodder gets its own "row" of solution candidates.
    #Each Row could contain several anagram possibilities

    if(len(letters)>9):
        print("Too many letters (", len(letters), ")to try an ANAGRAM. Sorry.")
        return(0)

    numAnafound = 0
    d = enchant.Dict("en_US")
    mylist = itertools.permutations(letters)
    #each letter is separate. Need to scrunch them together and the chk English dict
    for a in mylist:
        combo = ''.join(a)
        if (d.check(combo)):
            cfg.solTextSeq += "could be "+ combo.upper()+" \n"
            numAnafound += 1
            solRow.append(combo)

    cfg.solCandidates.append(solRow)
    return numAnafound





