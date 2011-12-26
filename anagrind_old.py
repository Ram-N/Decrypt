import itertools
import enchant
from nltk.corpus import wordnet

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

    print("Anag Parameters: starts at",cfg.anagrindIndex,            cfg.numAnagrindWords)

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
                cfg.numFods += 1
                cfg.fodList.append(fWords)
                print("Found one", cfg.solLen, w, fodLen)
            if fodLen >= cfg.solLen: #includes the exact len match case as well
                fodLen = 0
                fWords = ""
                break #done with j, move on to next i
            
    return(cfg.numFods)     



def identify_anagram_fodder2(cluewords,aG, grindWordIndex):
    """ Find the combination of letters that when Anagrammed, mean the definition """

    #remove the last token (it contains the length of the solution)
    cluewords.pop()

# Case 1a P-A-P: First, is it Part1, Anagrind Part 2
## Is it definition, anagrind, Fodder
    if     grindWordIndex >1:
        if     cfg.numWordsInClue > grindWordIndex:
            print("DAF or FAD")
            #identify part 1; words before Grind
            p2 = 0
            for w in cluewords:
                if w == aG:
                    p2=1
                    continue
                if p2==0:
                    cfg.part1Len += w.__len__() #add word lengths
                    cfg.part1.append(w)
                    #print ("Part1:",w,w.__len__())
                else:
                    cfg.part2Len += w.__len__() #add word lengths
                    cfg.part2.append(w)
                    #print ("Part2:",w)


# Case 2: PPA : Is it part1, Part2, Anagrind?
    if (cfg.numWordsInClue == grindWordIndex + (cfg.numAnagrindWords-1)): 
        print("DFA or FDA")

## Definition, Fodder, Anagrind
## Fodder, Definition, Anagrind
        
    endpoint = (-1) * cfg.numAnagrindWords #skip 0 or (0 & 1)
    print(endpoint, reversed(cluewords[0]),reversed(cluewords[1]))
    p1 = 0
    for w in reversed(cluewords[:endpoint]):    
        if (p1 == 0):
            cfg.part2Len += w.__len__() #add word lengths
            cfg.part2.append(w)
            print ("Part2:",w,cfg.part2Len)
            if cfg.part2Len == cfg.solLen:
                print("Found Fodder. Must be D-F-A")
                p1=1
        else:
            cfg.part1Len += w.__len__() #add word lengths
            cfg.part1.append(w)
            print ("Part1:",w)
# Need to add extra logic to check for FDA. Since Len(D) won't be SolLen, we need additional logic


# Case 3: APP : Is it Anagrind, part1, Part2
## Anagrind, Definition, Fodder
    if     grindWordIndex  == 1:
        print("A-F-D or A-D-F")

        # skip the initial ANAGRIND words
        startpoint = cfg.numAnagrindWords #skip 0 or (0 & 1)

        p2 = 0
        for w in cluewords[startpoint:]:
            if (p2 == 0):
                cfg.part1Len += w.__len__() #add word lengths
                cfg.part1.append(w)
                #print ("Part1:",w,cfg.part1Len)
                if cfg.part1Len == cfg.solLen:
                    print("Found Fodder.")
                    p2=1
            else:
                cfg.part2Len += w.__len__() #add word lengths
                cfg.part2.append(w)
                #print ("Part2:",w)



#we now have part1 and part2. Which is the fodder?
    fodderType = 3

    if cfg.solLen == cfg.part1Len:
        if cfg.solLen <> cfg.part2Len:
            fodderType = 1

    if cfg.solLen == cfg.part2Len:
        if cfg.solLen <> cfg.part1Len:
            fodderType = 2

    return fodderType




def check_if_full_anagram(fullclue):
    """ Are any of the AnagrInds present in the clue? """

    cluewords = fullclue.lower().split()
    anagfound =0
    defn = 0
    
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
    numFod = identify_anagram_fodder(cluewords)

    if numFod == 0:
        print("Fodder not found")

    if numFod:    
        defn = identify_definition(0) #which part of the clue is definition


    anafound = make_anagram(0)    
    
    return(anagfound)
## end of check if anagram ##





def    make_anagram(defn):    
    """ take the letters in each fodder and see if a valid word can be anagrammed """

#cfg.fodder and cfg.defwords are now known
    for f in cfg.fodList:
        print ("Trying ANAGRAM OF ",f)

#verify that fodder length and solLen match


#generate all valid Anagrams - solCandidates gets populated here
        anafound = generate_valid_anagrams(f)

# check if the meaning of foundsoln is one of the definition words
        check_candidates_against_definition()

#need something better below
    return anafound

                



def  check_candidates_against_definition():
    """ List has solCandidates. Check if the MEANING of any word in definition matches """

    for s in cfg.solCandidates:
        #print ("Trying candidate - ",s)
        mlist = store_meaning(s)

        for dw in cfg.defwords:
            #print ("definition:",dw)
            if mlist.count(dw) >0:
                print("Found it!!", s, "Matches Defintion")
        

def store_meaning(oneword):
    """ store the meaning in a list """

    for word_meaning in wordnet.synsets(oneword):
        #print word_meaning.definition
        return(word_meaning.definition)



def generate_valid_anagrams(letters):
    """ Using itertools to generate Anagrams. THen check against English dictionary"""



    if(len(letters)>9):
        print("Too many letters (", len(letters), ")to try an ANAGRAM. Sorry.")
        return(0)

    anafound = 0
    d = enchant.Dict("en_US")
    mylist = itertools.permutations(letters)
    #each letter is separate. Need to scrunch them together and the chk English dict
    for a in mylist:
        combo = ""
        for i in range(0, len(a)):
            combo += a[i]
        if (d.check(combo)):
            print combo 
            anafound = 1
            cfg.solCandidates.append(combo)
    return anafound   


def identify_definition(fodder):
    """ assign the part of clue to be definition, based on Anag fodder """

    if fodder == 1:
        print("DEFINITION of solution is:", cfg.part2)
        defn = 2
        cfg.defwords = cfg.part2

    if fodder == 2:
        print("DEFINITION of solution is:", cfg.part1)
        defn = 1
        cfg.defwords = cfg.part1


    if fodder == 3:
        print("DEFINIION could be", cfg.part1, "OR")
        print("DEFINITION of solution is:", cfg.part2)
        defn = 3
        cfg.defwords = cfg.part1
        cfg.defwords.append(cfg.part2)
        
    return 0


