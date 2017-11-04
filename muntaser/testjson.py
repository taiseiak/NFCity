import json

out_dict = {}
with open ('out.txt') as json_file:
	data = json.load(json_file)
	#print(data)
	for r in data['results']:
		print('platenumber: ' + r['plate'])
		out_dict['platenumber'] = r['plate']
		out_dict['spot'] = 1


#print(out_dict)
with open('jsonout.txt', 'w') as outfile:  
    json.dump(out_dict, outfile)

