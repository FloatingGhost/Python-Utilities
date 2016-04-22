#aiutils

##Artificial intelligence utilities

###NGram

The N-Gram model is a way of modelling a training corpus (text) into a set of
probabilities, P(W<sub>0</sub> | W<sub>-1</sub>, W<sub>-2</sub>...W<sub>-N</sub>).

So, for example, N=2 on "Cats sit, and cats run" would generate:
```
N=2
P(cats | <empty>) = 0.5
P(cats | and)     = 0.5
P(sit  | cats)    = 0.5
P(run  | cats)    = 0.5
P(and  | sit)     = 1
P(<end>| run)     = 1
```

####Usage

```python
from floatingutils.aiutils import NGram

corpus = "Cats sit, and cats run"

N = 2

#Build the model
model  = NGram(corpus, n)

#Get the probability of P(cats|and)
prob = model.getProb("cats", "and")
>>> prob = 0.5

#Generate a random possible string
string = mode.generate()
>>> string = "cats run" (or something that *could* be said)
```
