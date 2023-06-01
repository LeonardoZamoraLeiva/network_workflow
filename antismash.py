import os
import shutil
from move_rename import create_folder
import pandas as pd


def antismash_func(input_folder, output_folder):
    gbk_list = []
    for gbkfile in os.listdir(input_folder):
        gbk_list.append(gbkfile)

    for file in range(len(gbk_list)):
        try:
           #folder_to_create = '{}/{}'.format(output_folder, gbk_list[file])
           if gbk_list[file] not in os.listdir(output_folder):
                #create_folder(str(folder_to_create))
                antismash = 'antismash --genefinding-tool prodigal --cb-general --cb-knownclusters ' \
                            '--pfam2go --output-dir {}/{} {}/{}'.format(output_folder, gbk_list[file][0:-4],
                                                                        input_folder, gbk_list[file])
                print(antismash)
                os.system(antismash)

        except ValueError:
            print("{} can't be analyzed by AntiSMASH and should be removed from the analysis.")


def for_bigscape(folder_name, for_bigscape_folder, antismash_folder, project_folder):

    work_folder = '{}/{}'.format(antismash_folder, folder_name)
    df = pd.read_csv('{}/quality_final.csv'.format(project_folder))
    for index, row in df.iterrows():
        if row['strain'] == folder_name:

            for file in os.listdir(work_folder):
                if file.endswith('.gbk') and file[0:-4] != folder_name:
                    to_folder = '{}/{}_{}'.format(for_bigscape_folder, row['id'], file)
                    in_folder = '{}/{}'.format(work_folder, file)
                    with open(in_folder, 'r') as f_in:
                        with open(to_folder, 'w') as f_out:
                            shutil.copyfileobj(f_in, f_out)
