import os
from ftplib import FTP
from ftp_conection import FTP_Walker, ask_strain, StrainName
from unzip import unzipfunc
from prokka import prokkafunc
from antismash import antismash_func, for_bigscape
from bigscape_script import bigscape_func, modify_output

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
                ftp.retrbinary("RETR "+item, open(os.path.join(os.getcwd(), 'zip',item.split('/')[-1]), "wb").write)
                # it will print the file address
                print(item)


###          Unzip donwloaded files         #####
#from_folder = '{}/zip'.format(os.getcwd())
#to_folder = '{}/unzip'.format(os.getcwd())
#unzipfunc(from_folder, to_folder)

###          Prokka annotation         #####
unzipFolder = os.getcwd() + '/unzip'
prokkafunc(unzipFolder, os.getcwd())

###          antiSMASH analysis         #####
antismash_func()
for file in os.listdir('antismash'):
    for_bigscape(file)

###          bigscape run         #####
bigscape_func()
modify_output()