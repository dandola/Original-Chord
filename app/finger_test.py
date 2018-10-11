import ring
import config
import distance
import hashkey
import finger_table
import random
import ring
import json
import math
import main
import numpy as np



def test_lookup(keys=[]):
	k= config.NODES
	fail=0
	count_request=0
	list1=[]
	all_cost=[]
	for node in main.nodes:
		if node.status==True:
			for key in keys:
				count_request+=1
				print "node: ",node.keyID, " tim key: ", key
				t = node.lookup(key,duongdi=[])
				if isinstance(t, basestring) == True:
					fail+=1
				list1.append(int(t))
	max_value,min_value=0,0
	print list1
	if(len(list1)!=0):					
		mean=sum(list1)*1.0/len(list1)
		max_value=max(list1)
		min_value=min(list1)
	else:
		mean = 0
		print'mean: ',mean
	result = {'max': max_value,'list_cost':list1, 'min': min_value,'mean': mean,'requests': count_request,'fails': fail}
	return result

def test_finger():
	keys=[]
	b= "set_2000_keys_lookup.txt"
	with open(b,'r') as filedata:
		keys= json.load(filedata)
	print len(keys)
	a = "set_1024_nodes.txt"
	datas=[]
	with open(a,'r') as filedata:
		datas=json.load(filedata)
	result=[]
	i=0
	for data in datas:
		main.load(data)
		result_test= test_lookup(keys['keys'])
		name = "topo_" + str(config.NODES) + "_nodes_" + str(2000) + "_keys_lookup_with_" + str(i) +"%_faulty_nodes_original_chord.json"
		with open(name,"w") as fw:
			json.dump(result_test,fw)
		return json.dumps("ket thuc",indent=3)
		main.reset()
		i+=10
	return json.dumps("ket thuc",indent=3)