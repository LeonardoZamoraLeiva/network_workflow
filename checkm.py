import pandas as pd
import os
from move_rename import create_folder

def checkm_command(to_filter,checkm_out,rank,taxon):
    create_folder(checkm_out)

    taxonmywf_command = 'checkm taxonomy_wf -t 8 {} {} {} {}'.format(rank, taxon, to_filter, checkm_out)
    print(taxonmywf_command)
    os.system(taxonmywf_command)
    ''' 
    checkm qa requiere primero haber corrido el taxonomy_wf, ya que utiliza el archivo '.ms' que genera este ultimo.
    Por lo tanto, utiliza ccomo inputs el archivo '.ms' y la carpeta output del taxonomy_wf
    '''

    #path to ms file and output folder from the taxonomy_wf (output_folder is the same as before)
    ms_file = '{}/{}.ms'.format(checkm_out, taxon)
    """name and path for the output_file"""
    output_file = '{}/qa_{}.csv'.format(to_filter, taxon)
    qa_command = 'checkm qa {} {} -o 2 -t 8 --tab_table -f {}'.format(ms_file, checkm_out, output_file)
    print(qa_command)
    os.system(qa_command)


'''
use the qa output to filter the results
'''


def filter_strains(to_filter, taxon):
    strains_that_pass = []
    df = pd.read_csv('{}/qa_{}.csv'.format(to_filter, taxon), sep='\t',
                     usecols=['Bin Id', 'Marker lineage', '# contigs', 'Completeness', 'Contamination'])
    total_rows = len(df.index)

    for n in range(total_rows):
        if df.iloc[n][2] > 98.00 and df.iloc[n][3] < 2.00 and df.iloc[n][4] < 200:
            strains_that_pass.append(df.iloc[n][0])

    print(strains_that_pass)
    return strains_that_pass
