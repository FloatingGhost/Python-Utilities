from floatingutils.aiutils import NGram

corpus = "the cat sat on the mat, the cat ran"

def test_bigram():
  model = NGram(corpus, 2)
  assert( 0.5 == model.getProb("sat", "cat") )

def test_trigram():
  model = NGram(corpus, 3)
  assert ( 0.5 == model.getProb("ran", "the cat"))

