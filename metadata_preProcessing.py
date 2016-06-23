import json 
import gzip 
final_dic = {}

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
	except:
		pass
	
	final_dic.update({productId:temp})
	final_dic

def parse(path): 
	g = gzip.open(path, 'r') 
	for l in g: 
		yield (eval(l)) 
 
def main():
	global final_dic

	for row in parse("metadata.json.gz"): 
		preProcess(row)
	
	with open('metadata_parse.json', 'a') as outfile:
   		json.dump(final_dic,outfile)
	


main()