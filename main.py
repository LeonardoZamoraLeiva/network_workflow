import os
from ftplib import FTP
from ftp_conection import download_file, ask_strain
from unzip import unzipfunc
from checkm import checkm_command, filter_strains
from prokka import prokkafunc
from antismash import antismash_func, for_bigscape
from bigscape_script import bigscape_func, modify_output
from network import network_visualization_func
import pandas as pd

strain_of_analysis = 'vb1'
project_folder = '{}/{}'.format(os.getcwd(), strain_of_analysis)
download_folder = '{}/zip_for_{}'.format(project_folder, strain_of_analysis)
unzip_folder = '{}/unzip_for_{}'.format(project_folder, strain_of_analysis)
checkm_folder = '{}/checkm'.format(unzip_folder)
prokka_results_folder = '{}/prokka_{}'.format(project_folder, strain_of_analysis)
prokka_gbks_folder = '{}/prokka_gbks_{}'.format(project_folder, strain_of_analysis)
antismash_folder = '{}/antismash_for_{}'.format(project_folder, strain_of_analysis)
for_bigscape_folder = '{}/for_bigscape_{}'.format(project_folder, strain_of_analysis)
bigscape_output_folder = '{}/bigscape_results_{}'.format(project_folder, strain_of_analysis)
cutoffs = '0.3 0.6 0.7'

report_dict = {
    'strain_name': [],
    'Bin Id': [],
    'status': [],
    '#contigs': [],
    'completness': [],
    'contamination': []
}

'''###          Extract files from ncbi.refseq ftp         #####'''
host_address = 'ftp.ncbi.nlm.nih.gov'
user_name = 'anonymous'
password = 'leo.zamoraleiva@gmail.com'

strainCollection = []
ask_strain(strainCollection)
print(strainCollection)
ftp = FTP(host_address)
ftp.login(user=user_name, passwd=password)
for n in strainCollection:
    try:
        download_file(n)
    except ValueError:
        print('Unable to locate the file')

###          Unzip donwloaded files, analyze qualtity and filter        #####
taxon = 'Streptomyces'
rank = 'genus'
unzipfunc(download_folder, unzip_folder, report_dict)
checkm_command(unzip_folder, checkm_folder, rank, taxon)
strains_that_pass = filter_strains(unzip_folder, taxon)
print(len(strains_that_pass))

for strain in report_dict['Bin Id']:
    is_in = False
    for n in range(len(strains_that_pass)):
        if strain in strains_that_pass[n]:
            report_dict['status'].append('pass')
            is_in = True
            break
    if not is_in:
        report_dict['status'].append('failed')

df1 = pd.DataFrame(report_dict)
df2 = pd.read_csv('{}/qa_{}.csv'.format(unzip_folder, taxon),
                  usecols=['Bin Id', '# contigs', 'Completeness', 'Contamination'])
df3 = pd.merge(df1, df2, on=['Bin Id'], how='left')
df3.to_csv('{}/merge_test.csv'.format(project_folder), index=False)
print(df3)
df3.to_csv('{}/strains_report_test.csv'.format(project_folder), index=False)

###          Prokka annotation         #####
for strain in strains_that_pass:
    try:
        prokkafunc(strain, unzip_folder,prokka_results_folder, prokka_gbks_folder)
    except ValueError:
        print("{} can't be annotated".format(strain))

###          antiSMASH analysis         #####
antismash_func(prokka_gbks_folder, antismash_folder)
for folder in os.listdir(antismash_folder):
    for_bigscape(folder,for_bigscape_folder, antismash_folder)

###          bigscape run         #####
bigscape_func(for_bigscape_folder, bigscape_output_folder, cutoffs)
modify_output(bigscape_output_folder)

###       Network visualization      #####
network_folder = '{}/network_files'.format(bigscape_output_folder)
for folder, subfolder, files in os.walk(network_folder):
    for i in range(len(subfolder)):
        if "hybrids" not in subfolder[i] and 'transformed' in subfolder[i]:
            subfolder_full = '{}/{}'.format(network_folder, subfolder[i])
            for file in os.listdir(subfolder_full):
                if 'edges' in file:
                    file_full_path = '{}/{}'.format(subfolder_full, file)
                    network_visualization_func(file_full_path)
