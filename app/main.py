import node
import ring
import config
import distance
import hashkey
import finger_table
import random
import ring
import json
import sys
rings=[]
nodes=[]
sys.setrecursionlimit(25000)
def create_ring(ring_id):
	new_ring= ring.Ring(ring_id)
	new_ring.create(nodes)
	rings.append(new_ring)
	str ='tao ring thanh cong!!!'
	print str
	return str

def join(NodeID,NodeID_old):
	node_joined= None
	for nod in nodes:
		if NodeID_old==nod.NodeID:
			if nod.status==False:
				a='Node ',str(nod.NodeID),' khong hoat dong'
				print a
				return a
			node_joined= nod
			break
	if node_joined is None:
		print 'khong ton tai node joined: ', NodeID_old
		a= 'khong ton tai node joined: ' + str(NodeID_old)
		return a
	new_node = node.Node(NodeID)
	new_node.join(node_joined)
	nodes.append(new_node)
	# rings[0].nodes.append(new_node)
	return infor_nodes(new_node.NodeID)


def remove(NodeID):
	node=None
	for i in nodes:
		if NodeID== i.NodeID:
			if i.status==False:
				a='Node ',str(i.NodeID),' khong hoat dong'
				print a
				return a
			node=i
			break
	if node is None:
		print 'khong ton tai node co NodeID la: ', NodeID
		result= 'khong ton tai node co NodeID la: ' + str(NodeID)
		return result
	if node.remove():
		nodes.remove(node)
		rings[0].nodes.remove(node)
		return 'remove thanh cong'


def lookup(NodeID,keyID=None,data=None):
	duongdi=[]
	node_joined=None
	for node in nodes:
		if NodeID==node.NodeID:
			if node.status==False:
				a='Node ',str(node.NodeID),' khong hoat dong'
				print a
				return a
			node_joined= node
			break
	if node_joined is None:
		kq= 'khong co Node nao co ID: ' +  str(NodeID)
		return kq
	if keyID is None:
		keyID=hashkey.hashkey(data)
	result= node_joined.lookup(keyID,duongdi)
	if result==False:
		a= "lookup loi"
	else:
		a= "chi phi lookup la: " + str(result)
	return json.dumps(a, indent=3)


def insert(NodeID,data):
	duongdi=[]
	node_old=None
	for nod in nodes:
		if nod.NodeID==NodeID:
			if nod.status==False:
				a='Node ',str(nod.NodeID),' khong hoat dong'
				print a
				return a
			node_old=nod
			break
	if node_old is None:
		print 'khong ton tai node da tham gia co NodeID la: ', NodeID
		a= 'khong ton tai node da tham gia co NodeID la: ' + str(NodeID)
		return a
	return node_old.insert(data,duongdi)


def infor_nodes(node_id):
	if node_id==-1:
		list1=[] 
		i=0
		nod=nodes[0]
		while 1:
			a= {i:{'NodeID': nod.NodeID,'keyID': nod.keyID,'status': nod.status,'NodeID sucessor': nod.successor.NodeID,'NodeID predecessor': nod.predecessor.NodeID,'key-value': nod.managekey_value}}
			list1.append(a)
			i+=1
			nod= nod.successor
			if nod==nodes[0]:
				return json.dumps(list1,indent=4)
	for nod in nodes:
		if nod.NodeID==node_id:
			return nod.get_infor()
	print 'khong tim thay node co gia tri NodeID la: ', node_id
	return 'False'


def save():
	arr=[]
	arr_fail=[]
	for nod in nodes:
		if nod.managekey_value:
			for key_value in nod.managekey_value:
				if not(distance.distance(nod.m,nod.predecessor.keyID,key_value['key'],nod.keyID)):
					continue
				else :
					data= {'NodeID': nod.NodeID, 'data': key_value['value']}
					arr.append(data)
		if nod.status==False:
			arr_fail.append(nod.NodeID)

	data={
		'id_ring': rings[0].Id_Ring,
		'Nodes': [x.NodeID for x in nodes],
		'data': arr,
		'Node_false': arr_fail
		}
	a= 'data_'+ str(config.NODES) + '.txt'
	with open(a,'w') as filedata:
		print data
		json.dump(data,filedata)
		return True

def load(filedata):
	if rings ==[]:
		data=filedata
		# data=json.dumps(data)
		id_ring=data['id_ring']
		Nodes= data['Nodes']
		key_value=data['data']
		Node_false=data['Node_false']
		# tao ring
		new_ring= ring.Ring(id_ring)
		mean= new_ring.create(Nodes)
		rings.append(new_ring)
		# khoi tao key_value
		if key_value!=[]:
			for i in key_value:
				print i['data']
				print insert(i['NodeID'],i['data'])
		for nod in Node_false:
			print failure(nod)
		return True
	else: 
		print('da ton tai ring')
		return False



# moi mot node insert 5 data
def insert_data():
	for nod in nodes:
		if nod.status==True:
			for i in range(10):
				data=random.randint(1,2**20)
				insert(nod.NodeID,data)
	return 'hoan thanh insert'

	
def failure(NodeID):
	node=None
	for nod in nodes:
		if nod.NodeID==NodeID:
			node=nod
			break
	if node is None:
		a= "khong co node nao co NodeID = " + str(NodeID)
		return a
	if node.status== False:
		return "hoan thanh"
	else:
		node.status=False
		return "hoan thanh"

def reset():
	rings[:]=[]
	nodes[:]=[]
	return 'finished'


def count_fail_nodes():
	count=0
	for node in nodes:
		if node.status== False:
			count+=1
	str= "so luong node fail la: ", count
	return json.dumps(str, indent=3)

