import os
from move_rename import create_folder
import pandas as pd


def bigscape_func(input_folder, output_folder, cutoffs):
    create_folder(output_folder)
    os.system('bigscape.py -i {} -o {} -v --cutoffs {} --mibig --mix --clans-off'.format(input_folder,output_folder,cutoffs))

###revisar!!!
#def modify_output(bigscape_output_folder,domains_csv_file):
def modify_output(bigscape_output_folder):
    # definir carpetas
    original_folder = os.getcwd()
    os.chdir('{}/network_files'.format(bigscape_output_folder))
    root_dirs = next(os.walk('./'))[1]
    network_folders = str('./' + root_dirs[0])
    all_dirs = next(os.walk(network_folders))[1]

    # crear carpetas para cada tipo de BGC
    i = 0
    while i < len(all_dirs):
        folder = 'transformed' + all_dirs[i]
        os.mkdir(folder)
        folder_path = '{}/{}'.format(root_dirs[0], all_dirs[i])

        # Buscar files para utilizarlos como base para crear la tabla final
        for subdir, dirs, files in os.walk(folder_path):
            #name_final_b = ''
            for name in files:
                # busar y modificar ".tsv" files
                if name.startswith("Network") and not name.endswith('Full.tsv'):
                    #current_folder = str(all_dirs[i])
                    path = subdir + os.sep + name

                    # Modificar el archivo .tsv para utilizardo en gephi o algún otro visualizador
                    # Nombre final es "tipo_de_bgc"_nodes.csv

                    # a:crear dos columnas, ID y Label
                    a = pd.read_csv(path, sep='\t')
                    a2 = a.rename({'BGC': 'ID'}, axis=1)
                    a3 = a2[['ID', 'BiG-SCAPE class']].copy()
                    a3['label'] = a3['ID'].apply(lambda x: x.split('_')[0])
                    name_final_a = '{}/{}_nodes.csv'.format(folder, all_dirs[i])
                    a3.to_csv(name_final_a, index=False)

                # buscar y modificar ".network" files
                if name.endswith('.network'):
                    #current_folder = str(all_dirs[i])
                    path = subdir + os.sep + name

                    # b:crear dos columnas, Source y Target
                    b = pd.read_csv(path, sep='\t')
                    b2 = b.rename(
                        {'Clustername 1': 'Source', 'Clustername 2': 'Target', 'Squared similarity': 'Weight'}, axis=1)
                    b3 = b2[['Source', 'Target', 'Weight', 'Raw distance']].copy()
                    name_final_b = '{}/{}_{}_edges.csv'.format(folder, all_dirs[i], name[-13:-9])
                    b3.to_csv(name_final_b, index=False)


            '''for file in os.listdir(folder):
                if file.endswith('edges.csv'):
                    try:
                        #print(folder)
                        #print(file)
                        cutoff = file.split('_')[1]
                        # Modificar, agregar en modify_output para generar todos los archivos.
                        df1 = pd.read_csv('{}/G11C/{}'.format(original_folder, domains_csv_file), delimiter=',')
                        df2 = pd.read_csv('{}/{}'.format(folder, file), delimiter=',')
                        df3 = pd.merge(df1, df2, on=['Source'], how='outer')
                        df3.to_csv('{}/{}_edges_domains.csv'.format(folder, cutoff), index=False, sep='\t')
                        print(file)
                    except ValueError:
                        print('cant create this file')'''
        i += 1
    os.chdir(original_folder)



