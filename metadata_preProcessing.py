import json 
import gzip 
import redis


data_obj = redis.Redis("localhost", port=6379, db=2)

def preProcess(row):
	print row
	global final_dic
	temp = []
	productId = row["asin"]
	try:
		boughtTogether = row["related"]["bought_together"]
		for ele in boughtTogether:
			temp.append("b_t_"+ele)
		alsoBought = row["related"]["also_bought"]
		for ele in alsoBought:
			temp.append("a_b_"+ele)
		alsoViewed = row["related"]["also_viewed"]
		for ele in alsoViewed:
			temp.append("a_v_"+ele)
		data_obj.set(productId, temp)
	except:
		pass
	
	

def parse(path): 
	g = gzip.open(path, 'r') 
	for l in g: 
		yield (eval(l)) 
 
def main():
	count = 0
	for row in parse("metadata.json.gz"): 
		count+=1
		print count
		preProcess(row)


main()