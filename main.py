import sys
#sys.argv[x]
inputfile='all_inlinks.csv'
outputfile='output.html'
try:
	inputfile = sys.argv[1]
except IndexError:
	print("Default input.")

try:
	outputfile = sys.argv[2]
except IndexError:
	print("Default output.")

class Node:
	""" Every node in a group of anchor/alttext """
	destinations = list()
	destlen = 0
	def __init__(self,anchor):
		self.anchor = anchor
	def __eq__(self,other):
		if isinstance(other, self.__class__):
			return self.anchor == other.anchor
		else:
			return False
	def __ne__(self,other):
		return not self.__eq__(other)
	def __str__(self):
		return self.anchor
	def __repr__(self):
		return self.__str__()
	def addDest(self,dest):
		if dest not in self.destinations:
			self.destinations.append(dest)
			self.destlen+=1

nodes = list()
anchorTXT = "anchor"
alttextTXT = "alt text"
destTXT = "destination"
statusTXT = "status"
codeTXT = "status code"
indexeskey = [anchorTXT,alttextTXT,destTXT,statusTXT,codeTXT]
indexesval = [-1,-1,-1,-1,-1]
columnindexdone = False
nodo = Node("")
file = open(inputfile,'r')
for x in file.readlines():
	array = x.replace('"','').replace("\n",'').lower().split(',')
	if not columnindexdone:
		for i,y in enumerate(indexeskey):
			try:
				indexesval[i]=array.index(y)
				columnindexdone=True
			except ValueError:
				print("Value not found: "+y)
		print(str(indexesval))
		continue
	anchor = array[indexesval[indexeskey.index(anchorTXT)]]
	if not anchor:
		anchor = array[indexesval[indexeskey.index(alttextTXT)]]
	nodo = Node(anchor)
	encontrado = False
	for xnodo in nodes:
		if nodo==xnodo:
			encontrado=True
			xnodo.addDest(array[indexesval[indexeskey.index(destTXT)]])
			break
	if not encontrado:
		nodes.append(nodo)
file.close();
for nodo in nodes:
	if nodo.destlen>1:
		print(nodo.destlen)
		print(nodo)
		print(nodo.destinations)
		exit()
