anagrinds = list()
stopwords= []
charade_dict = dict()
cluetype_dict =  dict()

solnFile = "solutions.txt"

# for the clue in question
solCandidates = list()
defwords = list()

mode = ""

# these following inits are needed so that they are in cfg NameSpace
solLen = 0
part1Len = 0
part2Len = 0
numAnagrindWords = 0
anagrindIndex = 0
numFods = 0
fodList = []
fodStart = [] #index integer
fodEnd = [] #index integer


solTextSeq = ""
indivClueWordsSeq = ""
numWordsInClue = 0
clueWords = ""

nSolutionWords = 0
isSingleWordSolution = 0

def addLine(strSeq, newLineStr):
    strSeq += newLineStr + "\n"
    return(strSeq)
