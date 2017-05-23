import sys
import re
import hashlib
import csv
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
		self.origins = list()
		self.httpcode = list() #numcode
		self.status = list() #text status
		self.isanchor = list() #text status
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
	def addDest(self,dest,origin,code,status,isanchor):
		if dest not in self.destinations:
			self.destinations.append(dest)
			self.origins.append(origin)
			self.httpcode.append(code)
			self.status.append(status)
			self.isanchor.append(isanchor)
			self.destlen+=1
	def sortbyname(self):
		return self.anchor
	def sortbylen(self):
		return self.destlen

nodes = list()
anchorTXT = "anchor"
alttextTXT = "alt text"
destTXT = "destination"
originTXT = "source"
statusTXT = "status"
codeTXT = "status code"
typeTXT = "type"
indexeskey = [anchorTXT,alttextTXT,destTXT,statusTXT,originTXT,codeTXT,typeTXT]
indexesval = []
for i in range(len(indexeskey)):
	indexesval.append(-1)

columnindexdone = False
csvfile = open(inputfilename,"r")
inputfile = csv.reader(csvfile, delimiter=',') #open(inputfilename,'r')
for x in inputfile:
	array = list(map(lambda x:x.lower(),x))
	if not columnindexdone:
		print(array)
		for i,y in enumerate(indexeskey):
			try:
				indexesval[i]=array.index(y)
				columnindexdone=True
			except ValueError:
				print("Value not found: "+y)
		print(str(indexesval))
		continue
	if not array[indexesval[indexeskey.index(typeTXT)]]=='href':
		continue
	isanchor = True
	anchor = array[indexesval[indexeskey.index(anchorTXT)]]
	if not anchor:
		anchor = array[indexesval[indexeskey.index(alttextTXT)]]
		isanchor = False

	nodo = Node(anchor)
	encontrado = False
	for xnodo in nodes:
		if nodo == xnodo:
			encontrado = True
			xnodo.addDest(array[indexesval[indexeskey.index(destTXT)]],array[indexesval[indexeskey.index(originTXT)]],
				array[indexesval[indexeskey.index(codeTXT)]],array[indexesval[indexeskey.index(statusTXT)]],isanchor)
			break
	if not encontrado:
		nodes.append(nodo)
csvfile.close()

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
		for i,dest in enumerate(zip(nodo.destinations,nodo.origins,nodo.httpcode,nodo.status,nodo.isanchor)):
			finalrow += row
			finalrow = finalrow.replace("{{ROW}}",str(i))
			finalrow = finalrow.replace("{{ISANCHOR}}",str(dest[4]))
			finalrow = finalrow.replace("{{ORIGIN}}",dest[1])
			finalrow = finalrow.replace("{{DESTINATION}}",dest[0])
			finalrow = finalrow.replace("{{CODE}}",dest[2])
			finalrow = finalrow.replace("{{STATUS}}",dest[3])

		finaltable = table
		finaltable = finaltable.replace("{{ROWS}}",finalrow)
		finaltable = finaltable.replace("{{ISANCHORTITLE}}","alt?")
		finaltable = finaltable.replace("{{ORIGINTITLE}}","Origen")
		finaltable = finaltable.replace("{{DESTTITLE}}","Destino")
		finaltable = finaltable.replace("{{CODETITLE}}","Código")
		finaltable = finaltable.replace("{{STATUSTITLE}}","Status")
		
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
print("Done")