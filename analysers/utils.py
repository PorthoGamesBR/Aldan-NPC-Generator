import re

def find_pattern(pat : str, txt : str):
        M = len(pat)
        N = len(txt)
        if M > N:
                return [-1]
        indexes = []
        for i in range((N - M) + 1):
                j = 0
                
                while(j < M):
                        if(txt[i +  j] !=  pat[j]):
                                break
                        j+=1
                if (j == M):
                        print("\nPattern found at " + str(i) + "\n")
                        indexes.append(i)
        return indexes
    
def multisplit(*args, txt) -> list:
    string_to_split = "["
    for item in args:
        string_to_split += item
    string_to_split += "]"
    
    to_return = re.split(string_to_split, txt)
                
    return to_return

def unest_lists(ls : list):
        list_to_return = []
        last_type = ""
        for elm in ls:
                if hasattr(elm, '__iter__') and type(elm) != str:
                        un_ls = unest_lists(elm)
                        list_to_return += un_ls
                else:
                        list_to_return.append(elm)
        return list_to_return