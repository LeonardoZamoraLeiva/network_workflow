import ftplib
import os
from ftplib import FTP
from move_rename import create_folder

host_address = 'ftp.ncbi.nlm.nih.gov'
user_name = 'anonymous'
password = 'leo.zamoraleiva@gmail.com'
ftp = FTP(host_address)
ftp.login(user=user_name, passwd=password)


def StrainName(FTPpath):
    strain_name = []
    for item in range(len(ftp.nlst(FTPpath))):
        listPath = ftp.nlst(FTPpath)[item].split(os.sep)
        strain = listPath[5]
        strain_name.append(strain)
    return strain_name


def ask_strain(strainCollection):
    strains = False
    while not strains:
        strain = str(input('Please enter the strain you want (eg:Streptomyces_albidoflavus): '))
        strainCollection.append(strain)

        question = str(input('Want to add more strains? (Y/N): '))
        if 'n' in question.lower():
            strains = True


def download_file(main_folder, file_name):
    original_dir = os.getcwd()
    os.chdir('{}'.format(main_folder))
    create_folder(file_name)

    try:
        ftpwalk = ftp.nlst("genomes/refseq/bacteria/{}/{}".format(file_name, 'latest_assembly_versions'))
        strainName = StrainName("genomes/refseq/bacteria/{}/{}".format(file_name, 'latest_assembly_versions'))

        full_name = []
        for strain in strainName:
            full_name_strain = strain + '_genomic.fna.gz'
            full_name.append(full_name_strain)

        for item in ftpwalk:
            for j in full_name:
                if j[0:-15] in item:
                    # it is downloading the file
                    full_path = '{}/{}'.format(item, j)
                    try:
                        ftp.retrbinary("RETR " + full_path,
                                       open(os.path.join(os.getcwd(), file_name, full_path.split('/')[-1]),
                                            "wb").write)
                        # it will print the file address
                        print(full_path)
                    except ftplib.error_perm:
                        print('aca esta el error')

    except ftplib.error_temp as resp:
        if str(resp) == '450 No such file or directory':
            print('No files in this directory')
        else:
            raise


    os.chdir(original_dir)
