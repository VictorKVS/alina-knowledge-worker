"""Toy character BPE from Suhas Pai CH03 example, standard library only."""
from collections import Counter

CORPUS=["bat","cat","cap","sap","map","fan"]

def pairs(sequences):
    return Counter((a,b) for word in sequences for a,b in zip(word,word[1:]))

def merge(sequences,pair):
    out=[]
    for word in sequences:
        result=[]
        i=0
        while i<len(word):
            if i+1<len(word) and (word[i],word[i+1])==pair:
                result.append(word[i]+word[i+1]);i+=2
            else:
                result.append(word[i]);i+=1
        out.append(result)
    return out

def train(words=CORPUS,steps=2):
    seq=[list(w) for w in words]
    rules=[]
    for _ in range(steps):
        counts=pairs(seq)
        if not counts:break
        best=max(counts,key=lambda p:(counts[p],-len("".join(p)),tuple(-ord(c) for c in "".join(p))))
        rules.append((best,counts[best]))
        seq=merge(seq,best)
    return rules,seq

if __name__=="__main__":
    rules,seq=train()
    print("rules:",rules)
    print("sequences:",seq)
