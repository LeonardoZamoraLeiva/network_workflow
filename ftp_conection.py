import os
from ftplib import FTP

host_address = 'ftp.ncbi.nlm.nih.gov'
user_name = 'anonymous'
password = 'leo.zamoraleiva@gmail.com'
ftp = FTP(host_address)
ftp.login(user=user_name, passwd=password)


def FTP_Walker(FTPpath, localpath):

    os.chdir(localpath)
    current_loc = os.getcwd()
    for item in ftp.nlst(FTPpath):
        if not is_file(item):
            yield from FTP_Walker(item, current_loc)

        elif is_file(item):
            yield item
            current_loc = localpath
        else:
            print('this is a item that i could not process')

    os.chdir(localpath)
    return


def StrainName(FTPpath):
    strain_name = []
    for item in range(len(ftp.nlst(FTPpath))):
        listPath = ftp.nlst(FTPpath)[item].split(os.sep)
        strain = listPath[5]
        strain_name.append(strain)
    return strain_name


def is_file(filename):
    current = ftp.pwd()
    try:
        ftp.cwd(filename)
    except Exception as e:
        ftp.cwd(current)
        return True

    ftp.cwd(current)
    return False


def ask_strain(strainCollection):
    strains = False
    while not strains:
        strain = str(input('Please enter the strain you want (eg:Streptomyces_albidoflavus): '))
        strainCollection.append(strain)

        question = str(input('Want to add more strains? (Y/N): '))
        if 'n' in question.lower():
            strains = True


def download_file(file_name):
    ftpwalk = FTP_Walker("genomes/refseq/bacteria/{}/{}".format(file_name, 'latest_assembly_versions'), os.getcwd())
    try:
        strainName = StrainName("genomes/refseq/bacteria/{}/{}".format(file_name, 'latest_assembly_versions'))
        full_name = []
        for strain in strainName:
            full_name_strain = strain + '_genomic.fna.gz'
            full_name.append(full_name_strain)

        for item in ftpwalk:
            for strain in full_name:
                if strain in item:
                    # it is downloading the file
                    ftp.retrbinary("RETR " + item,
                                   open(os.path.join(os.getcwd(), 'zip', item.split('/')[-1]), "wb").write)
                    # it will print the file address
                    print(item)
    except:
        print("{} strain doesn't exist on refseq".format(file_name))
