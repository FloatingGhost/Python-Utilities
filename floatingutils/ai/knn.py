#!/usr/bin/env python3

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
      
