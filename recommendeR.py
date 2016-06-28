from gensim.models import Word2Vec

fname = 'data/models/user_local_context_v1_b.txt'

# 1.4M
# 1.9M
model = Word2Vec.load(fname)

#print model.most_similar( positive = ['C0312430027'], topn=100)

count = 0
for i in model.vocab:
    count+=1
    print count, i, model.most_similar( positive = [i], topn=10)