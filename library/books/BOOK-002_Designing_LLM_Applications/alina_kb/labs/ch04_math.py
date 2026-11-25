"""BOOK-002 CH04: independent numeric demonstrations, no LLM or training."""
from math import exp, log, sqrt

def cross_entropy_one_hot(probability):
    if not 0 < probability <= 1:
        raise ValueError("Correct-token probability must be in (0,1]")
    return -log(probability)

def perplexity_nats(losses):
    if not losses:
        raise ValueError("Cannot compute perplexity of empty list")
    return exp(sum(losses)/len(losses))

def softmax(xs):
    if not xs:
        raise ValueError("Empty score vector")
    m=max(xs)
    values=[exp(v-m) for v in xs]
    total=sum(values)
    return [v/total for v in values]

def toy_attention(query, keys, values):
    if not keys or len(keys)!=len(values) or not query:
        raise ValueError("Shape error")
    d=len(query)
    if any(len(k)!=d for k in keys):
        raise ValueError("Key/query mismatch")
    outdim=len(values[0])
    if any(len(v)!=outdim for v in values):
        raise ValueError("Value shapes differ")
    scores=[sum(q*k for q,k in zip(query,key))/sqrt(d) for key in keys]
    weights=softmax(scores)
    out=[sum(w*v[j] for w,v in zip(weights,values)) for j in range(outdim)]
    return weights,out

if __name__=="__main__":
    l1=cross_entropy_one_hot(0.1);l2=cross_entropy_one_hot(0.8)
    weights,out=toy_attention([1,0],[[1,0],[0,1]],[[2,0],[0,2]])
    print("losses:",round(l1,4),round(l2,4))
    print("weights:",[round(x,4) for x in weights])
    print("output:",[round(x,4) for x in out])
