#!/usr/bin/env python
import math
import os # Imports your specific operating system (os)
# import enchant
import urllib
from nltk.corpus import wordnet
import re
import sys

#import personal modules
import cfg # src file with globals
import fileutils
import textutils
import anagrind # another src file
import charade  # another src file

###########################################from urllib2 import *


def isValid_english(word):
    print(d.check(word))

def read_all_indicators():
      #URL LIBRARY
      ur = urlopen("https://raw.github.com/mhl/cryptic-crossword-indicators-and-abbreviations/master/indicators.yml")
      contents = ur.readlines()#readlines from url file
      fo = open("indicators.txt", "w")
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


def build_dictionary(filename, dic, reverse):
    #read the line in file indicators.txt
    fo = open(filename, "r")
    for line in fo:
        if ':' in line:
            create_dict_entry(dic, reverse, line)
    fo.close()#close text file



########### eo building dictionaries ############


def print_dictionary(dic):
    for key in dic:
        print key, dic.get(key)


def print_list(anagrinds):
    for a in anagrinds:
        print a


def meaning(oneword):
    for word_meaning in wordnet.synsets(oneword):
        print oneword.upper(),":", word_meaning.definition

def wprint(filename, text):
    f= open(filename,'at')
    f.writelines(text+ "\n")
    f.close()

def initfile(filename):
    f= open(filename,'w')
    f.write("\n")
    f.close()


############

def print_sol_length(cluewords):
#check if the solution length is given
    print "The number of words in the clue is:", len(cluewords)
    return(len(cluewords))


def get_clue():
    print("Input the cw clue")
    clue_string = raw_input("Enter something: ")
    return(clue_string)

def get_clue_from_file(filename):
    cl = list()
    print("Reading Clue File...")

    data = open(filename,'r').read()
    clue_string = data.splitlines()

    for c in clue_string:
        cl.append(c.rstrip())
        #print ("Clue is: ", c)
    return(cl)



def tokenize_clue(clue_string):
    # create a List of the clue words
    cfg.indivClueWordsSeq = clue_string.split(" ")
    cfg.numWordsInClue = len(cfg.indivClueWordsSeq) - 1


def get_total_letters_in_solution():
    return sol_length
    pass



def is_solution_length_given(cluestr):
    toks = cluestr.split(" ")
    last_token = toks[len(toks)-1]
    if(last_token.count("(") <=0) :
        print("Solution Length should be given within parentheses\n")
        return
    if(last_token.count(")") <=0) :
        print("Solution Length should be given within parentheses\n")
        return


    mid = last_token.rstrip(')').lstrip('(')
    print "Solution should be of length", mid
    digits = mid.split(",")
    for d in digits:
        if d.isdigit() <> 1:
            print ("Include only word-lengths and commas within parentheses\n")
            return



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

    #print "solution contains", num_solution_words, "word(s)"
    #print "digits", digits

    #insert the TotalLength in position 0 of the list
    solLength.insert(0,totSolLength)

    return solLength


def getNumSolWords(lTok):
    mid = lTok.lstrip("(").rstrip(")")
    cfg.nSolutionWords = mid.count(",") + 1
    if cfg.nSolutionWords == 1:
        cfg.isSingleWordSolution = 1

#message()
def message():
    again = raw_input("Do you want to play again? (Y/N) : ")
    if(again == "Y" or again == "y"):
        cwsolver()
    else:
        print "\n\n-------Thank you for playing!--------\n\n"
        exit()


##
##########################################

## See if any of the cluewords matches indicators
def identify_cluetype(fullclue):
    """ go thru clue hints dict and see if any matches in fullclue """

    typefound = 0

    ## Is an anagram indicated?
    anagfound = anagrind.check_if_full_anagram(fullclue)


    if cfg.mode == 'm':
        charade.print_clue_meaning()
        return 0

    # identify_definition()

    if (anagfound == 1):
        typefound = 1

    #need to see if dict_value contained in full clue
    cluewords = fullclue.split()
    for wd in cluewords:
        if(cfg.cluetype_dict.has_key(wd)):
                typefound = 1
                print("Clue type:", cfg.cluetype_dict.get(wd), "because of", wd)

    if(typefound==0):
        print ("Not quite sure what type of clue this is")

    return typefound

##########################################


def cw_solve(fullclue):

    cfg.solTextSeq = cfg.addLine(cfg.solTextSeq, fullclue + "\n\n")

    # Parse the clue (Make sure it is well formatted)
    error_check_clue(fullclue)

    tokenize_clue(fullclue)

    print( "Clue words", cfg.numWordsInClue)

    solLengthList = getSolutionWordLength(cfg.indivClueWordsSeq[-1])
    print "Sol Length List", solLengthList

    cfg.solLen = solLengthList[0] #total length

    getNumSolWords(cfg.indivClueWordsSeq[-1])
    if cfg.nSolutionWords == 1:
        print "Sol should be single", solLengthList[0], "letter word"
    else:
        print "Sol should contain", cfg.nSolutionWords, "words"

    #remove the last token (it contains the length of the solution)
    cfg.indivClueWordsSeq.pop()

# See if any of the cluewords matches indicators
    typefound = identify_cluetype(fullclue)

## See if any letters can be figured out
    charade.parse_clue(fullclue)

# Solution Options
# Present the best guess

    print "End - ", fullclue



def initialize_clue():
    del cfg.solCandidates[:]
    del cfg.defwords[:]

    cfg.numFods =0
    del cfg.fodList[:]
    del cfg.fodStart[:]
    del cfg.fodEnd[:]

    cfg.clueWords = ""
    cfg.solLen = 0
    cfg.numAnagrindWords = 0
    cfg.anagrindIndex = 0

    cfg.solTextSeq = ""

    cfg.indivClueWordsSeq = ""
    cfg.numWordsInClue = 0

    cfg.nSolutionWords = 0
    cfg.isSingleWordSolution = 0


###########################################
if __name__ == '__main__':
    
#d = enchant.Dict("en_US")
    typefound = 0
    mList = []

#Read the commandline flag
    if len(sys.argv) >1: #if a flag exists
        cfg.mode = sys.argv[1]

        if cfg.mode == 'a':    print("Append Anagram Indicator")
        if cfg.mode == 'c':    print("Append Charade Indicator")
        if cfg.mode == 'm':    print("Meanings only")
        if cfg.mode == 'addstop':    print("Append Stop Words")


## go through the list of indicators

#uncomment if github file needs to be read
#read_all_indicators()

    INDFILE = 'Data/indicators.txt'
    CLUETYPEFILE = 'Data/cluetypehints.txt'
    ANAGRINDFILE = 'Data/anagrinds.txt'
    STOPWORDSFILE = 'Data/stopwords.txt'
    CLUEFILE = 'Data/clue.txt'


    # build dictionary from local file (indicators.txt)
    build_dictionary(INDFILE,cfg.charade_dict,reverse=1)
# print_dictionary(charade_dict)

    # build dictionary from local file (indicators.txt)
    build_dictionary(CLUETYPEFILE, cfg.cluetype_dict,reverse=0)
    #print_dictionary(cluetype_dict)

    anagrind.read_anagrinds(ANAGRINDFILE, cfg.anagrinds)
    #print_list(anagrinds)

    cfg.stopwords= open(STOPWORDSFILE, 'r').read().splitlines()

    initfile(cfg.solnFile)

    # Read the clue
    # fullclue = get_clue()



    fullcluelist = get_clue_from_file(CLUEFILE)

    print "Number of clues read: ", len(fullcluelist)

    for fullclue in fullcluelist:
        initialize_clue()
        cw_solve(fullclue)
        wprint(cfg.solnFile,cfg.solTextSeq)

##########################################
