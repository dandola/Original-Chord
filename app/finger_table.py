import config
class Finger(object):
	"""docstring for Finger"""
	def __init__(self,keyID, index,successor=None):
		self.index=index
		start=keyID + 2**index
		if start > config.MAX_NODES:
			self.start = start - config.MAX_NODES
		else: self.start= start
		self.node= successor
		
	def get_info():
		print('Start: ',self.start)
		print('Node manage: ', self.node.get_info())