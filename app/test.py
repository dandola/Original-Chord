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

def fault(x):
	k= int(math.ceil(config.NODES*x))
	node_fail= random.sample(main.nodes,k)
	for nod in node_fail:
		nod.status=False


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
					all_cost.append(int(t))
				else:
					if t!=0:
						list1.append(t)
						all_cost.append(t)
	max_value,min_value=0,0
	print list1
	if(len(list1)!=0):					
		mean=sum(list1)*1.0/len(list1)
		max_value=max(list1)
		min_value=min(list1)
	else:
		mean = 0
		print'mean: ',mean
	if(len(all_cost)!=0):					
		all_mean=sum(all_cost)*1.0/len(all_cost)
	else:
		all_mean = 0
	result = {'max': max_value,'arr_cost':list1, 'min': min_value,'mean': mean,'fails': fail,'requests': count_request,'successes': len(list1),'overall_cost': all_mean,'max_overall_cost': max(all_cost)}
	return result


def format_data():
	for node in main.nodes:
		del node.managekey_value[:]

def insert(values=[]):
	count_request=0
	cost=[]
	for node in main.nodes:
		if node.status==True:
			for value in values:
				duongdi=[]
				print"insert data: ",value
				count_request+=1
				t = node.insert(value,duongdi)
				print"cost: ", t
				cost.append(t)
			format_data()
	if(len(cost)!=0):
		mean=sum(cost)*1.0/len(cost)
	else:
		mean=0
	result = {'max': max(cost), 'min': min(cost),'mean': mean,'requests': count_request}	
	return result

def test_insert():
	keys=[]
	b= "set_2000_keys_lookup.txt"
	with open(b,'r') as filedata:
		keys= json.load(filedata)
	a = "data_insert/insert_data_1024nodes.txt"
	datas=[]
	with open(a,'r') as filedata:
		datas = json.load(filedata)
	result=[]
	j=1
	for data in datas:
		main.load(data)
		result_test= insert(keys['keys'])
		a = str(j)+"nd:the_cost_insertion_1000_data_with_" + str(config.NODES) + "_nodes_original_chord.json"		
		with open(a,"w") as fw:
			json.dump(result_test,fw)
		main.reset()
		j+=1
	return json.dumps("ket thuc",indent=3)


def reset_true():
	for nod in main.nodes:
		if nod.status==False:
			nod.status=True
	return True



def test1():
	arr_num_nodes=[3600,4800]
	keys=[]
	b= "set_1000_keys_lookup.txt"
	with open(b,'r') as filedata:
		keys= json.load(filedata)
	datas=[]
	for node  in arr_num_nodes:
		config.NODES = node
		b="set_"+ str(node) +"_nodes.txt"
		with open(b,'r') as filedata:
			datas=json.load(filedata)
		main.load(datas)
		result_test= test_lookup(keys['keys'])
		name = "topo_" + str(config.NODES) + "_nodes_" + str(1000) + "_keys_lookup_with_original_chord.json"
		with open(name,"w") as fw:
			json.dump(result_test,fw)
		main.reset()
	return json.dumps("ket thuc",indent=3)







		
