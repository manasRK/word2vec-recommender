# Dumping Gensim Model data to a JSON file
# Original Author: Phi Van Thuy 
# Modified By: Vinay Kumar 
from gensim.models import Word2Vec

#Trained model
model_path = "user_local_context_v1.txt"

print "Loading model..."
model = Word2Vec.load(model_path)  # C binary format
print "Loading model: Done"

#Name of output file
f = open('cosine_skipgram.json','w')

f.write("{\n")

number_words = len(model.vocab)
#number_words = 10000
for i in range(0, number_words):
	stringA = model.vocab.items()[i][0]
	f.write("\n\"" + stringA.encode("utf-8") + "\":[\n")
	nearest_words = model.most_similar(positive=[stringA], negative=[],  topn=20)
	number_nearest_words = len(nearest_words)

	for j in range(0, number_nearest_words):
		f.write("{\"w\":\"" + nearest_words[j][0].encode("utf-8") + "\",\"d\":" + str(round(nearest_words[j][1], 3)) + "}")
		if j != number_nearest_words - 1:
			f.write(",\n")
		else:
			f.write("]")

	if i != number_words - 1:
		f.write(",\n")
	else:
		f.write("\n")

f.write("\n}\n")

f.close()

print "Finished!"
