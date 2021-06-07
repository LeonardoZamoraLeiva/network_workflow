import os
from ftplib import FTP
from ftp_conection import FTP_Walker, ask_strain, StrainName, download_file
from unzip import unzipfunc
from checkm import checkm_command, filter_strains
from prokka import prokkafunc_test
from antismash import antismash_func, for_bigscape
from bigscape_script import bigscape_func, modify_output
from network import network_visualization_func

#def settings_func():


###          Extract files from ncbi.refseq ftp         #####
host_address = 'ftp.ncbi.nlm.nih.gov'
user_name = 'anonymous'
password = 'leo.zamoraleiva@gmail.com'

ftp = FTP(host_address)
ftp.login(user=user_name, passwd=password)
strainCollection = []
ask_strain(strainCollection)
print(strainCollection)


for n in strainCollection:
    download_file(n)
'''    try:
        ftpwalk = FTP_Walker("genomes/refseq/bacteria/{}/{}".format(n, 'latest_assembly_versions'), os.getcwd())
        strainName = StrainName("genomes/refseq/bacteria/{}/{}".format(n, 'latest_assembly_versions'))
    
        full_name = []
        for strain in strainName:
            full_name_strain = strain + '_genomic.fna.gz'
            full_name.append(full_name_strain)
    
        for item in ftpwalk:
            for strain in full_name:
                if strain in item:
                    # it is downloading the file
                    ftp.retrbinary("RETR "+item, open(os.path.join(os.getcwd(), 'zip', item.split('/')[-1]), "wb").write)
                    # it will print the file address
                    print(item)
    except:
        print('{} does not exist on refseq database'.format(n))'''

###          Unzip donwloaded files         #####
taxon = 'Streptomyces'
rank = 'genus'
from_folder = '{}/zip'.format(os.getcwd())
to_folder = '{}/unzip'.format(os.getcwd())
checkm_folder = '{}/checkm'.format(to_folder)
unzipfunc(from_folder, to_folder)
checkm_command(to_folder, checkm_folder, rank, taxon)
strains_that_pass = filter_strains(to_folder, taxon)
print(len(strains_that_pass))

###          Prokka annotation         #####
unzipFolder = os.getcwd() + '/unzip'
for strain in strains_that_pass:
    try:
        prokkafunc_test(strain, to_folder)
    except ValueError:
        print("{} can't be annotated".format(strain))

###          antiSMASH analysis         #####
antismash_func()
for file in os.listdir('antismash'):
    for_bigscape(file)

###          bigscape run         #####
bigscape_func()
modify_output()

###       Network visualization      #####
network_folder = '{}/bigscape_output/network_files'.format(os.getcwd())
for folder, subfolder, files in os.walk(network_folder):
    for i in range(len(subfolder)):
        if "hybrids" not in subfolder[i] and 'transformed' in subfolder[i]:
            subfolder_full = '{}/{}'.format(network_folder, subfolder[i])
            for file in os.listdir(subfolder_full):
                if 'edges' in file:
                    file_full_path = '{}/{}'.format(subfolder_full, file)
                    network_visualization_func(file_full_path)
