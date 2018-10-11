import hashlib
def hashkey(NodeID):
	hashe_md5= hashlib.md5()
	hash_sha1= hashlib.sha1()
	hash_sha1.update(str(NodeID))
	key= int(hash_sha1.hexdigest(),16)
	return key

	

	