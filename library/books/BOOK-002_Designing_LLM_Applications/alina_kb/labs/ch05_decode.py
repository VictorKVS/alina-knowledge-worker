"""BOOK-002 CH05: toy probability decoding. Not a real LLM tokenizer or inference."""
import random

def normalize(scores):
    if any(s<0 for s in scores) or not scores or sum(scores)<=0:
        raise ValueError("Expected nonnegative probabilities with positive mass")
    total=sum(scores)
    return [s/total for s in scores]

def greedy(labels, probabilities):
    if len(labels)!=len(probabilities):raise ValueError("label/score length mismatch")
    p=normalize(probabilities)
    return labels[max(range(len(labels)),key=lambda i:p[i])]

def sample_top_k(labels, probabilities,k,seed=0):
    if len(labels)!=len(probabilities) or not 1<=k<=len(labels):raise ValueError("Invalid input")
    p=normalize(probabilities)
    ix=sorted(range(len(p)),key=lambda i:(-p[i],i))[:k]
    rng=random.Random(seed)
    return rng.choices([labels[i] for i in ix],weights=[p[i] for i in ix],k=1)[0]

def sample_top_p(labels, probabilities,threshold,seed=0):
    if len(labels)!=len(probabilities) or not 0<threshold<=1:raise ValueError("Invalid input")
    p=normalize(probabilities)
    ix=sorted(range(len(p)),key=lambda i:(-p[i],i))
    chosen=[];mass=0
    for i in ix:
        chosen.append(i);mass+=p[i]
        if mass>=threshold:break
    rng=random.Random(seed)
    return rng.choices([labels[i] for i in chosen],weights=[p[i] for i in chosen],k=1)[0]

if __name__=="__main__":
    labels=["INGEST_NEW","REVIEW","QUARANTINE"];p=[0.6,0.3,0.1]
    print("greedy",greedy(labels,p))
    print("topk2",sample_top_k(labels,p,2))
    print("topp0.8",sample_top_p(labels,p,0.8))
