import itertools
from nltk.corpus import wordnet
#import enchant
import anagrind
import cfg # src file with globals

############parsing####################
def parse_clue(fullclue):

    cluewords = fullclue.split()
    for wd in cluewords:
        if(cfg.charade_dict.has_key(wd)):
            print(wd, " could indicate ", cfg.charade_dict.get(wd))
        #    generate_valid_anagrams(word)
        #isValid_english(wd)
        #meaning(wd)
    print ('\n')




# is this word a charade word? How many options?
    #create charade clue words list
    #create charade_cand_list
#permute them all
# see if the solLen matches
# get defn
# does meaning match?





def  print_clue_meaning():
    ''' For each word in the Clue print its NLTK meaning.'''
    print ("Meaning of Clue:", cfg.indivClueWordsSeq)

    for cW in cfg.indivClueWordsSeq:
        print(myutils.store_meaning(cW))
