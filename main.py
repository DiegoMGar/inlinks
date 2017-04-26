import sys
import re
import hashlib
#sys.argv[x]
inputfilename='all_inlinks.csv'
outputfilename='html/index.html'
try:
	inputfilename = sys.argv[1]
except IndexError:
	print("Default input.")


class Node:
	""" Every node in a group of anchor/alttext """
	destlen = 0
	def __init__(self,anchor):
		self.anchor = anchor
		self.destinations = list()
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
	def sortbyname(self):
		return self.anchor
	def sortbylen(self):
		return self.destlen

nodes = list()
anchorTXT = "anchor"
alttextTXT = "alt text"
destTXT = "destination"
statusTXT = "status"
codeTXT = "status code"
indexeskey = [anchorTXT,alttextTXT,destTXT,statusTXT,codeTXT]
indexesval = [-1,-1,-1,-1,-1]
columnindexdone = False
inputfile = open(inputfilename,'r')
for x in inputfile.readlines():
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
inputfile.close();

bodyfile = open("html/resources/plantilla.html","r")
body = bodyfile.read()
bodyfile.close()

collapsefile = open("html/resources/collapse.html","r")
collapse = collapsefile.read()
collapsefile.close()

tablefile = open("html/resources/table.html","r")
table = tablefile.read()
tablefile.close()

rowfile = open("html/resources/row.html","r")
row = rowfile.read()
rowfile.close()

finalcollapse=""
nodes.sort(key=Node.sortbylen,reverse=True)
contador = 0
for nodo in nodes:
	if nodo.destlen>1:
		contador+=1
		m = hashlib.md5()
		m.update(nodo.anchor.encode('utf-8'))
		collapseid = m.hexdigest()
		finalcollapse+=collapse

		finalrow = ""
		for i,dest in enumerate(nodo.destinations):
			finalrow += row
			finalrow = finalrow.replace("{{ROW}}",str(i))
			finalrow = finalrow.replace("{{DESTINATION}}",dest)
			finalrow = finalrow.replace("{{CODE}}",'0')
			finalrow = finalrow.replace("{{STATUS}}",'0')

		finaltable = table
		finaltable = finaltable.replace("{{ROWS}}",finalrow)
		finaltable = finaltable.replace("{{DESTTITLE}}","Destino")
		finaltable = finaltable.replace("{{CODETITLE}}","Código http")
		finaltable = finaltable.replace("{{STATUSTITLE}}","Status code")
		
		finalcollapse = finalcollapse.replace("{{COLLAPSETEXT}}",finaltable)
		finalcollapse = finalcollapse.replace("{{DUPLICATED}}",str(nodo.destlen))
		finalcollapse = finalcollapse.replace("{{COLLAPSEID}}",collapseid)
		finalcollapse = finalcollapse.replace("{{COLLAPSETITLE}}",nodo.anchor)
		#print(nodo.destlen)
		#print(nodo)
		#print(nodo.destinations)

body = body.replace('{{LISTADO}}',finalcollapse);
body = body.replace('{{TOTALDUPLICATED}}',str(contador));

outputfile = open(outputfilename,"w")
outputfile.write(body);
outputfile.close()