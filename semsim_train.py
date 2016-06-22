
import os
from nltk.corpus import stopwords
import re

stop = stopwords.words('english')
import gensim
import string
from unidecode import unidecode


def pre_process(m):
    m = unidecode(m)
    m = m.lower().strip() #normalize
    #print m
    #m=re.sub("[^a-zA-Z]", " ",m) #keep text only
    m="".join(l for l in m if l not in string.punctuation) #remove punctuation
    m=[i for i in m.split() if i not in stop] #remove stopwords
    #m=m.split()
    #print m
    return m

#iterator on Amazon Reviews  
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        count = 0
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                count +=1
                line = pre_process(line)
                print count
                yield line.split()
                
#directory for training
inputfile="output/" # output directory
#model save name
fname="output_models/model_22062016.txt"


sentences = MySentences(inputfile)
model = gensim.models.Word2Vec(sentences, min_count=10, workers=8, negative=10, sg=1, size = 300, sample=1e-5, hs=1) #v6 
model.init_sims(replace=True)
model.save(fname)

