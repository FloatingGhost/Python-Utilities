#!/usr/bin/env python
__author__ = 'Hannah Ward'
__package__ = "magicutils"

import random
import math
from floatingutils.log import Log

def listtostr_(n):
  """Turn [1,2,3] to "1 2 3"""
  k = ""
  for i in n:
    k += i + " "
  return k.strip()

class NGram: 
  """Class for an N-Gram model of a natural language corpus"""
  def __init__(self, corpus, n, debug=False, model=None):
    self.log = Log()
    
    if debug:
      self.log.setLevel(self.log.DEBUG)
    
    self.n = n
    self.log.info("Initialising {}-Gram model...".format(n))   
    
    if model:
      self.model = model
    else:
      if type(corpus) == type([]):
        self.buildModel(corpus)
      else:
        self.buildModel([corpus])
    self.log.info("{}-Gram model ready for use".format(self.n))

  def buildModel(self, list_corpus):
    """Build a model from a list of strings"""
    #Pad out the message
    corpus = "" 

    self.log.info("Creating N-Gram model from {} string{}".format(len(list_corpus),
                                                 "s" if len(list_corpus)>1 else ""))

    for i in list_corpus:
      #Remove punctuation
      i = i.replace(","," ").replace("."," ")

      corpus += " <s> "*(self.n-1) + i + " <s> "*(self.n-2)+" <end>"
    corpus = corpus.strip().lower()
    nlen = []
    self.log.info("Splitting corpus into {} length strings".format(self.n))
    corpus = [x for x in corpus.split(" ") if x != '']
    for i in range(len(corpus)-1):
      nlen.append(corpus[i:i+self.n])
    if len(nlen) > 6000:
      nlen = nlen[:6000]
    qqq = len(nlen)
    self.log.info("Processing {} {}-length strings".format(len(nlen), self.n))
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
    
    self.log.info("Calculating probabilities...")
    #calculate probs
    percentages = range(10, 101, 10)
    for w in givenWords:
      p = givenWords.index(w) / qqq
      p = 100*p
      if p > percentages[0]:
        self.log.info("{}% done...".format(p))
        percentages = percentages[1:]
      occurances = [x for x in nlen if x[:-1] == w]
      for x in occurances:
        y = x[-1] ##endword
        endswith = [z for z in occurances if z[-1] == y]
        ##Count number of occurrences
        try:
          modelAdd = [x[-1], w, 1.0 / (1+len(occurances)-len(endswith))]
        except ZeroDivisionError:
          ##Prob must be 1
          modelAdd = [x[-1],w,1.0]
        self.model.append(modelAdd)

    self.log.info("{}-Gram model built!".format(self.n))

  def generate(self):
    """Generate a possible message from the model"""
    self.log.info("Generating a possible string...")
    try:
      m = "<s>"
      while m.split(" ")[-1] != "<end>":
        m += " " + random.choice(self.getAllFromGiven(m.split(" ")[-self.n+1:])) 
      self.log.info("Generated!")
      return m.replace("<s>","").replace("<end>","")
    except IndexError:
      return "Could not generate... not enough data!"
  def getAllFromGiven(self, given):
    """Get all instances of x, where (given, x) is a member of the model"""
    j = []
    for i in self.model:
      if i[1] == given:
        j.append(i[0])
    return j

  def getProb(self, word, given):
    """Get P(word|given)"""
    ##Find P(word | given)
    for i in self.model:
      g = listtostr_(i[1])
      if i[0] == word and given == g:
        return i[2]
    return 0

class KNearest:
  """Class to allow use of a K-Nearest Neighbour classifier"""

  def __init__(self, data, labels, k=1):
    self.log = Log()
    self.log.info("Starting KNearest clustering with n={}".format(k))
    self.data = data
    self.k = k
    if not ( type(data) == list and  type(labels) == list ):
      self.log.error("KNearest data must be a list")
    if len(data) != len(labels):
      self.log.error("Data and labels have different dimensions!")
    if type(data[0]) != list:
      self.log.error("KNearest requires a list for each co-ordinate") 
    if type(data[0][0]) not in  [float, int]:
      self.log.error("KNearest can only deal with numbers")
    if self.k > len(data):
      self.log.warning("K is greater than the number of data points")
    self.labels = labels
    self.numDims = len(data[0])
    self.log.info("KNearest classfier ready.")

  def distanceFunction(self, a, b):
    """Default euclidian distance"""
    self.log.debug("Calculating difference between {} and {}".format(a,b))
    x = 0
    for i in range(len(a)):
      dimdif = abs(a[i] - b[i])
      x += dimdif ** 2

    return math.sqrt(x)

  def _distanceMatrix(self, point):
    self.log.info("Calculating distance matrix...")
    return [self.distanceFunction(point, i) for i in self.data]

  def classify(self, point):
    if len(point) != self.numDims:
      self.log.error("Point to classify is of different dimensions to training data")

    self.log.info("Classifying {}...".format(point))
    mat = self._distanceMatrix(point)
    sortedmat = sorted(mat)
    l = {}
    for i in range(self.k):
      c = sortedmat[i]
      ind = mat.index(c)
      lab = self.labels[ind]  
      if lab in l:
        l[lab] += 1
      else:
        l[lab] = 1
    ##Return most common label
    return max(l, key=l.get)  
      
