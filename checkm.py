import pandas as pd
import os
from move_rename import create_folder


def checkm_command(to_filter, checkm_out, rank, taxon):
    create_folder(checkm_out)
    taxonmywf_command = 'checkm taxonomy_wf -t 64 {} {} {} {}'.format(rank, taxon, to_filter, checkm_out)
    print(taxonmywf_command)
    os.system(taxonmywf_command)
    #checkm qa requiere primero haber corrido el taxonomy_wf, ya que utiliza el archivo '.ms' que genera este ultimo.
    #Por lo tanto, utiliza ccomo inputs el archivo '.ms' y la carpeta output del taxonomy_wf
    #path to ms file and output folder from the taxonomy_wf (output_folder is the same as before)
    ms_file = '{}/{}.ms'.format(checkm_out, taxon)
    #name and path for the output_file
    output_file = '{}/qa_{}.csv'.format(to_filter, taxon)
    qa_command = 'checkm qa {} {} -o 2 -t 8 --tab_table -f {}'.format(ms_file, checkm_out, output_file)
    print(qa_command)
    os.system(qa_command)


#use the qa output to filter the results
def filter_strains(analysis_strain,contigs,completness,contamination):
    strains_that_pass = []
    df = pd.read_csv('{}/quality_merge.csv'.format(analysis_strain),
                     usecols=['Bin Id', 'Marker lineage', 'contigs_quast', 'Completeness', 'Contamination'])
    total_rows = len(df.index)
    new_file = []

    for n in range(total_rows):
        if df.iloc[n][2] > completness and df.iloc[n][3] < contamination and df.iloc[n][4] < contigs:
        #if df.iloc[n][2] > 98.00 and df.iloc[n][3] < 2.00:
            strains_that_pass.append(df.iloc[n][0])
            new_file.append((df.iloc[n][0], 'pass'))
            print((df.iloc[n][0], 'pass'))
        else:
            new_file.append((df.iloc[n][0], 'failed'))

    pass_failed_list = pd.DataFrame(new_file)
    pass_failed_list.columns = ['Bin Id', 'status']
    quality_final = pd.merge(df, pass_failed_list, on='Bin Id', how='left')
    quality_final.rename(columns={'Bin Id': 'strain'}, inplace=True)
    df2 = pd.read_csv('{}/all_strains.csv'.format(analysis_strain))
    quality_final2 = pd.merge(quality_final, df2, on='strain', how='right')
    quality_final2 = quality_final2[['id',  'species', 'strain', 'Marker lineage', 'Completeness', 'Contamination',
                                     'contigs_quast', 'status']]
    
    quality_final2.to_csv('{}/quality_final.csv'.format(analysis_strain), index=False)
    return (strains_that_pass)


def quast_quality(unzip_folder):
    quast_list = ''
    for file in os.listdir(unzip_folder):
        if file.endswith('.fna'):
            quast_list = quast_list + ' ' + '{}/{}'.format(unzip_folder, file)

    quast_command = 'quast.py {} -o {}/quast'.format(quast_list, unzip_folder)
    os.system(quast_command)


def merge_quality_checkM_quast(unzip_folder, strain_of_analysis,taxon):
    # Merge quality test (checkm and quast) into a unique quality file
    contigs_quast = []
    csv_file = pd.read_csv('{}/quast/report.tsv'.format(unzip_folder), delimiter='\t')
    all_file = pd.DataFrame(csv_file)
    all_file.columns = all_file.columns.str.replace('IMG_taxon', 'IMG-taxon')
    for i in all_file:
        contigs_quast.append((i, all_file[i][12]))
    quast_final = pd.DataFrame(contigs_quast[1:], columns=['Bin Id', 'contigs_quast'])
    qa_checkm = pd.read_csv('{}/qa_{}.csv'.format(unzip_folder,taxon), delimiter='\t')
    qa_checkm_data = pd.DataFrame(qa_checkm)
    print(qa_checkm_data)
    quality_merge = pd.merge(qa_checkm_data, quast_final, on= 'Bin Id', how='left')
    

    df0 = pd.read_csv('{}/all_strains.csv'.format(strain_of_analysis))
    id = pd.DataFrame(df0)
    #id = pd.DataFrame(columns=['id', 'strain'])
    id2 = id.rename({'strain': 'Bin Id'}, axis=1)
    quality_merge = pd.merge(quality_merge, id2, on= 'Bin Id', how='left')

    quality_merge.to_csv('{}/quality_merge.csv'.format(strain_of_analysis), index=False)