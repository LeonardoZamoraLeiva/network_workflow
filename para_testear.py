import json
import os

import requests

strain = 'G11C_PacBio_Illumina_Flye_Pilon_09102020'

json_file = requests.get('https://prism.adapsyn.com/api/task/8325cbce7827fa01ade350e14f34bbc1/results/file')
all_file = json.loads(json_file.text)


if strain in all_file['prism_results']['input']['filename']:
    print('here it is')
    to_search_list = []
    to_search_init = all_file['prism_results']['clusters']
    '''[0]['orfs'][0]['sequence']'''
    #to_search = to_search_init[2::]
    #to_search = 'QAEGNPLALVELARAADGRE'
    for i in range(len(to_search_init)):
        for j in range(len(to_search_init[i]['orfs'])):
            try:
                to_search_list.append(to_search_init[i]['orfs'][j]['sequence'])
            except:
                print ('doesnt exist')




folder = 'g11c_test/g11c'
found_list = 0
for file in os.listdir(folder):
    if file.startswith('045') and file.endswith('gbk'):
        full_path = '{}/{}'.format(folder, file)
        with open(full_path, 'r') as cluster:
            count = 0
            for line in cluster:
                count += 1
                for i in range(len(to_search_list)):
                    if to_search_list[i][1:7] in line or to_search_list[i][-7:-1] in line:
                        print(file)
                        print(line)
                        print (to_search_list[i])
                        found_list += 1

print (len(to_search_list))
print (found_list)