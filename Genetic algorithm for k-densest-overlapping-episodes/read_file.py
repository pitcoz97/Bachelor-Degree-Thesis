#Read the 4 real datasets and create the temporal graph


from datetime import date, time



def read(filename):

	with open(filename, 'r', encoding='utf-8') as f:
		file = f.readlines()
		data = []
		for row in file:
			data.append(row.strip())
	return data




#READ STUDENTS
#10000 edges, 889 nodes, 1000 ts

def students_dataset():

	filename_st = 'Temporal_network_data/real data/students.txt'

	print('Importing \'Students\' dataset...')
	students_data = read(filename_st)

	edges = []
	for el in students_data:
		el = el.strip().split(' ')
		edges.append((int(el[2]), int(el[3])))
	
	i = 0
	t = 0
	TS = {}
	while i < len(edges):
		for j in range(10):
			if t not in TS:
				TS[t] = []
			TS[t].append(edges[i])	
			i += 1
		t += 1
	return TS




#READ ENRON
#6245 edges, 1143 nodes, 815 ts

def enron_dataset():

	filename_enron = 'Temporal_network_data/real data/enron_mod.txt'

	print('Importing \'Enron\' dataset...')
	data_enron = read(filename_enron)

	enron_edges = []
	for el in data_enron:
		el = el.strip().split(' ')
		u = int(el[2])
		v = int(el[3])
		if u != v:
			enron_edges.append((int(el[2]), int(el[3])))

	i = 0
	t = 0
	TS = {}

	while i < len(enron_edges):
		if t < 540:
			for j in range(8):
				if t not in TS:
					TS[t] = []
				TS[t].append(enron_edges[i])	
				i += 1
		else:
			for j in range(7):
				if t not in TS:
					TS[t] = []
				TS[t].append(enron_edges[i])	
				i += 1
		t += 1

	return TS




#READ TWITTER 
# 11868 edges, 4605 nodes, 9968 ts

def twitter_dataset():

	filename_tw = 'Temporal_network_data/real data/twitter.txt'

	print('Importing \'Twitter\' dataset...')
	data_twitter = read(filename_tw)

	twitter_edges = []
	for el in data_twitter:
		el = el.strip().split(' ')
		u = int(el[2])
		v = int(el[3])
		if u != v:
			twitter_edges.append((u, v))

	i = 0
	t = 0
	TS = {}

	while i < len(twitter_edges):
		if t < 1900:
			for j in range(2):
				if t not in TS:
					TS[t] = []
				TS[t].append(twitter_edges[i])	
				i += 1
		else:
			if t not in TS:
				TS[t] = []
			TS[t].append(twitter_edges[i])	
			i += 1
		t += 1

	return TS




#READ FACEBOOK
#10000 edges, 4117 nodes, 9984 ts   

def facebook_dataset():
	filename_tw = 'Temporal_network_data/real data/facebook.txt'

	print('Importing \'Facebook\' dataset...')
	data = read(filename_tw)

	edges = []
	dates= []

	for row in data:

		el = row.strip().split('\"')
		data = el[1].strip().split(' ')
		day = data[0].strip().split('-')
		giorno = date(int(day[0]), int(day[1]), int(day[2]))
		hour = data[1].strip().split(':')
		ora = time(int(hour[0]), int(hour[1]), int(hour[2]))
		edge = el[2].strip().split(' ')
		d = (giorno, ora)
		u = int(edge[0])
		v = int(edge[1])
		if u != v:
			edges.append((u, v))
			dates.append(d)


	diz = create_dates_index(dates)
	TS = create_TS(edges, dates, diz)
	return TS


def create_dates_index(dates):
	new = {}
	i = 0
	for date in dates:
		if date not in new:
			new[date] = i
			i += 1
	return new


def create_TS(edges, dates, dates_indexed):
	TS_diz = {}
	i = 0
	for date in dates:
		ind = dates_indexed[date]
		if ind not in TS_diz:
			TS_diz[ind] = []
		TS_diz[ind].append(edges[i])
		i += 1
	return TS_diz
