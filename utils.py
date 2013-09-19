def  write_list_to_file(fname, lst):
  fo = open(fname, "a+") #append
  for w in lst:
    fo.write("%s\n" % w)
  fo.close()


def  write_dict_to_file(fname, _dict):
    fo = open(fname, "a+") #append
    for k,v in _dict.items():
        fo.write(" %s , %s\n " % (k , v))
    fo.write("\n")
    fo.close()


def   print_dict(dct):
  print "\n\nStarting to Print Dictionary \n\n\n"
  for k,v in dct.items():
    print k,v

def   print_list(lst):
    for l in lst:
        print l

def print_dictionary(dic):
    for key in dic:
        print key, dic.get(key)



