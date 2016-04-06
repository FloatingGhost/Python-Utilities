#!/usr/bin/env python
import string as st 
def stringToInt(string):
  l = st.printable
  a = {}
  for i in l:
    a[i] = 0
  
  for i in string:
    if i in l:
      a[i] += 1
  props = []
  for i in l:
    print("{} is {}".format(i, a[i]))
    props.append(a[i]/len(string))
  return [len(string)] + props

