from floatingutils.reddit import Reddit

r = Reddit()

def test_getsub():
  assert ( None != r.getSub("funny") )
