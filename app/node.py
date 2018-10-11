import ring
import config
import distance
import hashkey
import finger_table
import random
import ring
import json
manage_key=[]
class Node(object):
	"""Node"""
	def __init__(self,NodeID):
		self.NodeID=NodeID
		self.keyID = NodeID
		self.m=config.M
		self.successor= None
		self.predecessor= None
		self.managekey_value=[]
		self.finger=[]
		self.status=True


	"""tim kiem successor"""
	def closest_preceding_node(self,keyID):
		for i in range(self.m-1,-1,-1):
			if(distance.distance(self.m,self.keyID,self.finger[i].node.keyID, keyID)):
				if self.finger[i].node.status==False:
					continue
				return self.finger[i].node
		return self



	"""tim predecessor cua id"""
	def find_predecessor(self, keyID):
		node = self
		start=self
		while not(distance.distance(self.m,node.keyID,keyID,node.successor.keyID) or keyID == node.successor.keyID):
			node =node.closest_preceding_node(keyID)
			if node.keyID==start.keyID:
				return self
			start=node
		return node


	def find_successor(self,keyID,duongdi=[]):
		if(distance.distance(self.m,self.keyID,keyID,self.successor.keyID) or keyID==self.successor.keyID):
			if self.successor.status==False:
				return False
			return self.successor
		else:
			node= self.closest_preceding_node(keyID)
			if node.keyID==self.keyID:
				return False
			duongdi.append(node.NodeID)
			return node.find_successor(keyID,duongdi)

	"""khoi tao bang finger table cua node"""
	def init_finger_table(self,n):
		for i in range(self.m):
			node_finger=finger_table.Finger(self.keyID, i)
			self.finger.append(node_finger)
		self.finger[0].node= n.find_successor(self.finger[0].start)
		if self.finger[0].node==False or self.finger[0].node.predecessor.status==False:
			return False
		self.successor= self.finger[0].node  
		self.predecessor= self.successor.predecessor
		self.predecessor.successor=self
		self.successor.predecessor= self
		for i in range(self.m-1):
			if(distance.distance(self.m,self.keyID,self.finger[i+1].start,self.finger[i].node.keyID) or self.finger[i+1].start==self.finger[i].node.keyID):
				self.finger[i+1].node = self.finger[i].node
			else:
				self.finger[i+1].node= n.find_successor(self.finger[i+1].start)
				if self.finger[i+1].node==False:
					break
		return True



	""" cap nhat node n vao cac finger table khac"""
	def update_others(self):
		p=self
		for i in range(self.m):
			if(not distance.distance(config.M, p.keyID,((self.keyID-2**i)%(2**config.M)),p.successor.keyID) or not(((self.keyID-2**i)%(2**config.M))==p.keyID)):		
				p = self.find_predecessor((self.keyID-2**i)%(config.MAX_NODES))
				if(p.successor.keyID==(self.keyID-2**i)%(config.MAX_NODES)):
					p=p.successor
			p.update_finger_table(self,i)


	"""update bang table"""
	def update_finger_table(self,n,i):
		if(distance.distance(self.m, self.keyID, n.keyID, self.finger[i].node.keyID) or n.keyID==self.finger[i].start):
			if(not distance.distance(self.m,self.keyID,n.keyID,self.finger[i].start) or n.keyID==self.finger[i].start):
				# print 'update finger node: ', self.NodeID,' tai vi tri thu: ',i,' voi node finger la:',n.keyID
				self.finger[i].node=n
			p=self.predecessor
			if p.keyID == n.keyID:
				return True
			p.update_finger_table(n,i)
		elif self.keyID==n.keyID:
			p=self.predecessor
			if p.keyID == self.keyID:
				return True
			p.update_finger_table(n,i)




	"""gan key-value cho new node"""
	def set_key_value(self):  
		node_successor=self.successor
		if node_successor.status==False:
			return False
		if node_successor.managekey_value:
			for i in range(len(node_successor.managekey_value)):
				if distance.distance(self.m, node_successor.managekey_value[i]['key'],self.keyID,node_successor.keyID) or node_successor.managekey_value[i]['key']==self.keyID:
					obj= node_successor.managekey_value[i]
					self.managekey_value.append(obj)
					node_successor.managekey_value.remove(obj)
					return True
		else:
			return True


	def join(self,n=None):
		if(n!=None):

			if self.init_finger_table(n)==False:
				return False

			# print'---------------NEXT-------------'
			if self.set_key_value()==False:
				print "set_key_value failed!!!"
				return True
			# print'---------------NEXT-------------'
			self.update_others()
		else:
			print('node_goc_id: ',self.NodeID)
			for i in range(self.m):
				node_finger= finger_table.Finger(self.keyID,i)
				node_finger.node= self
				self.finger.append(node_finger)
			self.predecessor=self
			self.successor=self
	

	
	def insert(self,value,duongdi=[]):
		duongdi.append(self.NodeID)
		keyID= hashkey.hashkey(value)
		if(distance.distance(self.m,self.predecessor.keyID,keyID, self.keyID) or keyID==self.keyID):
			if self.managekey_value:
				for key_value in self.managekey_value:
					if key_value['key']==keyID:
						key_value['value']= value
						kq= {'duong di': duongdi,'NodeID': self.NodeID,'key-value': key_value}
						cost=len(duongdi)
						return cost

			key_value={'key': keyID, 'value':value}
			self.managekey_value.append(key_value)
			kq= {'duongdi': duongdi,'NodeID': self.NodeID,'key-value': key_value}
			cost= len(duongdi)
			return cost
		else:
			node= self.find_successor(keyID,duongdi)
			if node==False:
				return False
			return node.insert(value,duongdi)



	def fix_finger(self,n,i):
    		if self.finger[i].node.keyID==n.keyID:
				self.finger[i].node=n.successor
				p=self.predecessor
				if p.keyID==n.keyID:
    					return True
				p.fix_finger(n,i)



	def remove(self):
		node_successor= self.successor
		node_predecessor= self.predecessor
		if node_successor.status==False or node_predecessor.status==False:
			return False
		for key_value in self.managekey_value:
			node_successor.managekey_value.append(key_value)
		node_successor.predecessor=node_predecessor
		node_predecessor.successor= node_successor
		for i in range(self.m): 
			if self.keyID >= 2**i:
				p=self.find_predecessor(self.keyID - 2**i)
			else:
				p= self.find_predecessor(self.keyID - 2**i + 2**self.m)
			p.fix_finger(self,i)
		return True


	def lookup(self, keyID,duongdi=[]):
		value= None
		duongdi.append(self.NodeID)
		if(distance.distance(self.m,self.predecessor.keyID,keyID,self.keyID) or self.keyID==keyID):
			for key_value in self.managekey_value:
				if key_value['key']==keyID:
					# print 'gia tri data la: ', key_value['value']
					kq={'duongdi':duongdi,'key':key_value['key'],'data': key_value['value'],'thuoc Node': self.NodeID}
					cost=len(duongdi)-1
					# print json.dumps(kq, indent=3)
					return cost
			kq={'duongdi':duongdi,'key':keyID,'data': None,'thuoc Node': self.NodeID}
			cost=len(duongdi)-1
			# print json.dumps(kq, indent=3)
			return cost
		else:
			node = self.find_successor(keyID,duongdi)
			if node==False:
				print "lookup false"
				cost = str(len(duongdi) -1)
				return cost
			return node.lookup(keyID,duongdi)
		


	def get_infor(self):
		print '-----------------------------------------------------------------'
		print 'NodeID: ', self.NodeID,' keyID : ',self.keyID
		print 'NodeID_successor: ',self.successor.NodeID
		print 'NodeD_predecessor: ',self.predecessor.NodeID
		print 'thong tin quan ly key-value: '
		if self.managekey_value:
			print self.managekey_value
		else:
			print 'manageKey-value rong'
		print '---------------------------finger table-------------------------'
		print 'index------------------------------start---------------------------------successor-NodeID-----'
		for fin in self.finger:
			print fin.index,'--------', fin.start,'------------',fin.node.NodeID
		print '---------------------------end------------------------------------'
		a={
		'NodeID': self.NodeID,
		'keyID': self.keyID,
		'NodeID successor': self.successor.NodeID,
		'NodeID predecessor': self.predecessor.NodeID,
		'manage key-value': self.managekey_value,
		}
		return json.dumps(a,indent=4)


		
	


	