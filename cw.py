def meaning(oneword):
    for word_meaning in wordnet.synsets(oneword):
        print word_meaning.definition



def print_sol_length(cluewords):
#check if the solution length is given
    print "The number of words in the clue is:", len(cluewords)
    return(len(cluewords))


def get_clue():
    print("Input the cw clue")

    clue_string = raw_input("Enter something: ")
    print "you entered ", clue_string
    return(clue_string)

def get_clue_from_file(filename):
    cl = list()
    print("Reading Clue File...")

    data = open(filename,'r').read()
    if ( len(data.splitlines()) > 1):
        print("Multiple clues. Let's just go with the first one.")
    clue_string = data.splitlines()

    for c in clue_string:
        cl.append(c.rstrip())
        print ("Clue is: ", c)
    return(cl)



def tokenize_clue(clue_string):
    # create a List of the clue words
    cluewords = clue_string.split(" ")
    print "Clue:", cluewords
    numwords = len(cluewords)
    print numwords

    for item in cluewords:
        print item

    return(cluewords)



def isValid_english(word):
    print(d.check(word))




def read_all_indicators():
      #URL LIBRARY
      from urllib2 import *
      ur = urlopen("https://raw.github.com/mhl/cryptic-crossword-indicators-and-abbreviations/master/indicators.yml")
      contents = ur.readlines()#readlines from url file
      fo = open("indicators.txt", "w")#open test.txt
      for line in contents:
          #print "writing %s to a file" %(line,)
          fo.write(line) #write lines from url file to text file
          create_dict_entry(line)
      fo.close()#close text file
##########


#if key doesn't exist, create entry
#if key exists, append value
def    addindicator_to_dictionary(dic,ind, value):
    dic.setdefault(ind, []).append(value)



# if line is a valid entry, then add it to the dict
def     create_dict_entry(dic,reverse,line):
#parse line into its components
# create a List of the clue words
    words = line.split(":")
    key = words[0].lstrip()    
    try:
        value= words[1].rstrip('\n').lstrip()
        # print ind
    except:
        print "no value"

    if reverse == 1:
        addindicator_to_dictionary(dic,value,key)
    else:
        addindicator_to_dictionary(dic,key,value)


def build_dictionary(filename,dic,reverse):
    #read the line in file indicators.txt
    fo = open(filename, "r") 
    for line in fo:
        if ':' in line:
            create_dict_entry(dic, reverse, line)
    fo.close()#close text file




def print_dictionary(dic):
    for key in dic:
        print key, dic.get(key)



def print_list(anagrinds):
    for a in anagrinds:
        print a


########### eo building dictionaries ############


def get_total_letters_in_solution():
    return sol_length
    pass



def is_solution_length_given(cluestr):
    toks = cluestr.split(" ")
    last_token = toks[len(toks)-1]
    if(last_token.count("(") <=0) :
        print("Solution Length should be given within parentheses\n")
        sys.exit("retry")
    if(last_token.count(")") <=0) :
        print("Solution Length should be given within parentheses\n")
        sys.exit("retry")
    
    mid = last_token.rstrip(')').lstrip('(')
    print "Solution should be of length", mid
    digits = mid.split(",")
    for d in digits:
        if d.isdigit() <> 1:
            print ("Include only word-lengths and commas within parentheses\n")
            sys.exit("retry")
    

def error_check_clue(fullclue):
    print(fullclue)
    is_solution_length_given(fullclue)
    #numwords = print_sol_length(fullclue)



def getSolutionWordLength(lastTok):
    """ create a numeric array with solution lengths """

    print lastTok
    solLength = list()
    totSolLength = 0

    mid = lastTok.lstrip("(").rstrip(")")
    digits = mid.split(",")
    for d in digits:
        totSolLength += int(d)
        solLength.append(int(d))

    num_solution_words = mid.count(",") + 1

    print "solution contains", num_solution_words, "word(s)"
    print "digits", digits

    #insert the TotalLength in position 0 of the list
    solLength.insert(0,totSolLength)

    return solLength


def getNumSolWords(lTok):
    mid = lTok.lstrip("(").rstrip(")")
    return(mid.count(",")+1)

############parsing####################
def parse_clue(cluewords):

    for wd in cluewords:
        if(charade_dict.has_key(wd)):
            print(wd, " could indicate ", charade_dict.get(wd))
        else:
            if(len(wd)>=3):
                print("Meaning of Solution could be",wd)

        #    generate_valid_anagrams(word)
        isValid_english(wd)
        meaning(wd)
        print ('\n')
    

##########################################

## See if any of the cluewords matches indicators
def identify_cluetype(fullclue):
    """ go thru clue hints dict and see if any matches in fullclue """

    typefound = 0

    ## Is an anagram indicated?              
    anagfound = anagrind.check_if_full_anagram(fullclue)


    # identify_definition()            

    if (anagfound == 1): 
        typefound = 1

    #need to see if dict_value contained in full clue
    cluewords = fullclue.split()
    for wd in cluewords:
        if(cluetype_dict.has_key(wd)):
                typefound = 1
                print("Clue type:", cluetype_dict.get(wd), "because of", wd)

    if(typefound==0):
        print ("Not quite sure what type of clue this is")

    return typefound

##########################################


def cw_solve(fullclue):

    print ("\n\n Next clue")
# Parse the clue (Make sure it is well formatted)
    error_check_clue(fullclue)

    clue = tokenize_clue(fullclue)

    cfg.numWordsInClue = len(clue) - 1

    print "Clue words", cfg.numWordsInClue

    solLengthList = getSolutionWordLength(clue[len(clue)-1])
    print "Sol Length List", solLengthList


    cfg.solLen = solLengthList[0] #total length

    numWordsInSol = getNumSolWords(clue[len(clue)-1])
    if numWordsInSol == 1:
        print "Sol should be single", solLengthList[0], "letter word"
    else:
        print "Sol should contain", numWordsInSol, "words"

#remove the last token (it contains the length of the solution)
    clue.pop()

## See if any of the cluewords matches indicators
    typefound = identify_cluetype(fullclue)

## See if any letters can be figured out
#parse_clue(clue)

# Solution Options
# Present the best guess

    print "End - ", fullclue



def initialize_clue():
    del cfg.solCandidates[:]
    del cfg.part1[:]    
    del cfg.part2[:]    
    del cfg.defwords[:]
    del cfg.fodderwords[:]

    cfg.numWordsInClue = 0
    cfg.solLen = 0
    cfg.part1Len = 0
    cfg.part2Len = 0
    cfg.numAnagrindWords = 0
    cfg.anagrindIndex = 0


###########################################
#def cwsolver():
import math
import os #Imports your specific operating system (os)
os.system("cls")    #Windows based systems us
import enchant
import urllib
from nltk.corpus import wordnet
import re
import sys

import anagrind # another src file
import cfg # src file with globals


###########################################
d = enchant.Dict("en_US")
charade_dict = dict()
cluetype_dict =  dict()
typefound = 0

## go through the list of indicators

#uncomment if github file needs to be read
#read_all_indicators()

# build dictionary from local file (indicators.txt)
build_dictionary("indicators.txt",charade_dict,reverse=1)
#print_dictionary(charade_dict)

# build dictionary from local file (indicators.txt)
build_dictionary("cluetypehints.txt",cluetype_dict,reverse=0)
#print_dictionary(cluetype_dict)

anagrind.read_anagrinds("anagrinds.txt",cfg.anagrinds)
#print_list(anagrinds)

# Read the clue 
#fullclue = get_clue()
fullcluelist = get_clue_from_file("clue.txt")

print "# clues is: ", len(fullcluelist)

for fullclue in fullcluelist:
    initialize_clue()
    cw_solve(fullclue)

##########################################





#message()
def message():
		again = raw_input("Do you want to play again? (Y/N) : ")
		if(again == "Y" or again == "y"):
			cwsolver()
		else:
			print "\n\n-------Thank you for playing!--------\n\n"
			exit()


##




# http://stackoverflow.com/questions/6418785/scraping-english-words-using-python
# english_words = [tok for tok in tokens if d.check(tok)]


# Get a file-like object for the Python Web site's home page.
#f = urllib.urlopen("http://www.python.org")
# Read from the object, storing the page's contents in 's'.
#s = f.read()
#f.close()


# how to do error checking in Python 
