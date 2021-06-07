import os
from antismash import antismash_func, for_bigscape
from bigscape_script import bigscape_func, modify_output
from network import network_visualization_func

#antismash_func()
#for file in os.listdir('antismash_test_out'):
#    for_bigscape(file)


#bigscape_func()
modify_output()

print(os.getcwd())
network_folder = '{}/bigscape_output_test/network_files'.format(os.getcwd())
#network_folder = os.getcwd()
for folder, subfolder, files in os.walk(network_folder):
    for i in range(len(subfolder)):
        if "hybrids" not in subfolder[i] and 'transformed' in subfolder[i]:
            subfolder_full = '{}/{}'.format(network_folder, subfolder[i])
            for file in os.listdir(subfolder_full):
                if 'edges' in file:
                    file_full_path = '{}/{}'.format(subfolder_full, file)
                    network_visualization_func(file_full_path)
