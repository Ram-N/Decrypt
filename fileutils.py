
def wc(filename):
    """
    Returns the number of characters, words and lines in a file.
    The result is a tuple of the form (#characters, #words, #lines)
    """
    
    data = open(filename,'rb').read()
    return (len(data), len(data.split()), len(data.splitlines()))


def wprint(filename, text):
    f= open(filename,'at')
    f.writelines(text+ "\n")
    f.close()

def initfile(filename):
    '''Blank out the file if it exists'''
    f= open(filename,'w')
    f.write("\n")
    f.close()


