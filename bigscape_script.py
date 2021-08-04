import os
from move_rename import create_folder
import pandas as pd


def bigscape_func(input_folder, output_folder, cutoffs):
    create_folder(output_folder)
    os.system('bigscape.py -i {} -o {} -v --cutoffs {} --mibig --clans-off'.format(input_folder,output_folder,cutoffs))

###revisar!!!
def modify_output(bigscape_output_folder):
    # definir carpetas
    original_folder = os.getcwd()
    os.chdir('{}/network_files'.format(bigscape_output_folder)
    root_dirs = next(os.walk('./'))[1]
    network_folders = str('./' + root_dirs[0])
    all_dirs = next(os.walk(network_folders))[1]

    # crear carpetas para cada tipo de BGC
    i = 0
    while i < len(all_dirs):
        folder = all_dirs[i] + '_transformed'
        os.mkdir(folder)
        folder_path = root_dirs[0] + os.sep + all_dirs[i]

        # Buscar files para utilizarlos como base para crear la tabla final
        for subdir, dirs, files in os.walk(folder_path):
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
                    name_final_a = folder + os.sep + all_dirs[i] + '_nodes.csv'
                    a3.to_csv(name_final_a, index=False)

                # buscar y modificar ".network" files
                elif name.endswith('.network'):
                    #current_folder = str(all_dirs[i])
                    path = subdir + os.sep + name

                    # b:crear dos columnas, Source y Target
                    b = pd.read_csv(path, sep='\t')
                    b2 = b.rename(
                        {'Clustername 1': 'Source', 'Clustername 2': 'Target', 'Squared similarity': 'Weight'}, axis=1)
                    b3 = b2[['Source', 'Target', 'Weight', 'Raw distance']].copy()

                    name_final_b = folder + os.sep + all_dirs[i] + '_' + name[-13:-9] + '_edges.csv'
                    b3.to_csv(name_final_b, index=False)

        i += 1
    os.chdir(original_folder)
