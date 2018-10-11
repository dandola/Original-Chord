def distance(m,a,b,c):
	# print('a=',a,'b=',b,'c= ',c)
	if a==b or b==c:
		return False
	if a<b and b<c:
		return True
	elif a==c: return True
	else:
		if a<c:
			dis1= c-a
		else:
			dis1= c + 2**m - a
		if a < b:
			dis2= b-a
		else:
			dis2= b+ 2**m -a
			if dis2 > dis1: return False
		if b<c:
			dis3= c-b
		else:
			dis3= c + 2**m -b
			if dis3 > dis1: return False
		# return True
		if (dis1 == dis2 + dis3): return True
		else: return False
