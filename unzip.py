import os
import shutil
import gzip
import pandas as pd

def create_strains_file(strainOfAnalysis, unzipFolder):
    count = 1
    species_strain_list = [('id', 'strain', 'species')]
    for strain in os.listdir(unzipFolder):
        name = strain.rsplit('.',1)[0]
        toAdd = ('{}'.format(count), name, name)
        species_strain_list.append(toAdd)
        count = count + 1 

    df = pd.DataFrame(species_strain_list)
    df.to_csv('{}/all_strains.csv'.format(strainOfAnalysis), header=False, index=False)


# To unzip files. This func. can continue even with problems in the unziping
# This list store the files that cant be unziped to download them manually if necessary
def new_unzip_func(from_folder, to_folder, strain_of_analysis):
    not_unzip_list = []
    species_strain_list = [('species', 'strain', 'id')]
    #add strains to the list added by the user
    count = 1
    for strain in os.listdir(to_folder):
        name = strain.rsplit('.',1)[0]
        comb_species_strain = (name, name,'user_{}'.format(count))
        species_strain_list.append(comb_species_strain)
        count = count + 1 

    
    for dir, subdir, file in os.walk(from_folder):
        count = 1
        for i in file:
            species = dir.split('/')[-1]
            strain = i[0:-7]
            # Here we store the tuple combination of species and strain to easy lecture file
            comb_species_strain = (species, strain, count)
            species_strain_list.append(comb_species_strain)
            with gzip.open('{}/{}'.format(dir, i), 'rb') as f_in:
                with open('{}/{}'.format(to_folder, i[0:-3]), 'wb') as f_out:
                    try:
                        shutil.copyfileobj(f_in, f_out)
                    except:
                        not_unzip_list.append('{}/{}'.format(dir, i))
                    f_in.close()
                    f_out.close()
            count =+ 1 
    if len(not_unzip_list) > 0:
        print(not_unzip_list)
    else:
        print("All files were unziped successfully")
    # Here we generate the strains file (with the respective species name)
    df = pd.DataFrame(species_strain_list)

    df.to_csv('{}/all_strains.csv'.format(strain_of_analysis), header=False, index=False)
