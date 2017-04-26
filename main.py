file = open('all_inlinks.csv','r')
data = file.readlines()
for x in data:
	array = x.replace('"','').replace("\n",'').split(',')
	print "linea: "+str(array)
file.close();