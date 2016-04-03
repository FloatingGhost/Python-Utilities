#!/usr/bin/env python3
import random


def listtostr(n):
  k = ""
  for i in n:
    k += i + " "
  return k.strip()

class NGram:
  def __init__(self, corpus, n, debug=False):
    self.debug = debug
    self.n = n
    if type(corpus) == type([]):
      self.buildModel(corpus)
    else:
      self.buildModel([corpus])
  def buildModel(self, list_corpus):
    #Pad out the message
    
    corpus = "" 
    for i in list_corpus:
      #Remove punctuation
      i = i.replace(","," ").replace("."," ")

      corpus += " <s> "*(self.n-1) + i + " <s> "*(self.n-2)+" <end>"
    corpus = corpus.strip().lower()
    if self.debug:
      print(corpus)
    nlen = []
    corpus = [x for x in corpus.split(" ") if x != '']
    for i in range(len(corpus)-1):
      nlen.append(corpus[i:i+self.n])
    self.model = []   
    endWords = []
    givenWords = []
    for i in nlen:
      word = i[-1]
      given = i[:-1]
      if word not in endWords:
        endWords.append(word)
      if given not in givenWords:
        givenWords.append(given)

    #calc probs
    for w in givenWords:
      occurances = [x for x in nlen if x[:-1] == w]
      for x in occurances:
        y = x[-1] ##endword
        endswith = [z for z in occurances if z[-1] == y]
        ##Count number of occs
        try:
          modelAdd = [x[-1], w, 1.0 / (1+len(occurances)-len(endswith))]
        except ZeroDivisionError:
          ##Prob must be 1
          modelAdd = [x[-1],w,1.0]
        self.model.append(modelAdd)

  def generate(self):
    m = "<s>"
    while m.split(" ")[-1] != "<end>":
      m += " " + random.choice(self.getAllFromGiven(m.split(" ")[-self.n+1:])) 
    return m.replace("<s>","").replace("<end>","")
     
  def getAllFromGiven(self, given):
    j = []
    for i in self.model:
      if i[1] == given:
        j.append(i[0])
    return j

  def getProb(self, word, given):
    ##Find P(word | given)
    for i in self.model:
      g = listtostr(i[1])
      if i[0] == word and given == g:
        return i[2]
    return 0

