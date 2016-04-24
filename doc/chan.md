#chan

##A Wrapper to basc\_py4chan

###FourChan

This is simply a representation of a 4chan board.

####Usage

```python
from floatingutils.chan import FourChan

#Tell the API to go get /g/
board = FourChan("g")

posts = board.getPosts(limit=10)
>>> posts = [4ChanBord...]
```
