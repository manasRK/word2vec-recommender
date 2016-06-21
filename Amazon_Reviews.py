import gzip
import simplejson

def parse(filename):
  f = gzip.open(filename, 'r')
  entry = {}
  for l in f:
    l = l.strip()
    colonPos = l.find(':')
    if colonPos == -1:
      yield entry
      entry = {}
      continue
    eName = l[:colonPos]
    rest = l[colonPos+2:]
    entry[eName] = rest
  yield entry


count=0
for e in parse("C:\Users\Manas\Desktop\Text Analytics Product_SMAS\Data\Amazon Reviews Dataset\Arts.txt.gz"):
  count=count+1
  print count,": ",simplejson.dumps(e)