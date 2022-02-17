import re

def find_pattern(pat : str, txt : str):
        M = len(pat)
        N = len(txt)
        if M > N:
                return -1
        indexes = []
        for i in range((N - M) + 1):
                j = 0
                
                while(j < M):
                        if(txt[i +  j] !=  pat[j]):
                                break
                        j+=1
                if (j == M):
                        print("Pattern found at " + str(i))
                        indexes.append(i)
        return indexes
    
def multisplit(*args, txt) -> list:
    string_to_split = "["
    for item in args:
        string_to_split += item
    string_to_split += "]"
    
    to_return = re.split(string_to_split, txt)
                
    return to_return