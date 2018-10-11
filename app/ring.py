import config
import random
import node
import main
class Ring(object):
	"""docstring for ClassName"""
	def __init__(self,Id_ring):
		self.Id_Ring= Id_ring
		self.nodes=[]
		self.Max_Nodes= config.MAX_NODES


	def create(self,nodes):
		list1=[]
		if nodes == []:
			key=1461501637330902918203684832716283019655932
			part= int(2**160/config.NODES)
			list1= range(key, 2**160, part)
			# list1.append(key)
		else:
			list1=nodes
		for i in range(len(list1)):
			n= node.Node(list1[i])
			print("node thu ",i," node-id: ", n.NodeID,'keyID: ',n.keyID)
			if(len(self.nodes)==0):
				n.join()
			else: n.join(self.nodes[i-1])
			self.nodes.append(n)
			main.nodes.append(n)
		return True
		

	def info(self):
		print('information: ')
		
		
	
	
		