import os
import shutil
from move_rename import create_folder


def antismash_func():
    output_folder = str(os.getcwd()+'/antismash')
    prokka_folder = os.getcwd()+'/prokka'

    gbk_list = []
    for gbkfile in os.listdir(prokka_folder):
        gbk_list.append(gbkfile)

    for file in range(len(gbk_list)):
        folder_to_create = 'antismash/{}'.format(gbk_list[file])
        create_folder(str(folder_to_create))
        antismash = 'antismash  --genefinding-tool prodigal --cb-general --cb-knownclusters ' \
                    '--pfam2go {}/{} --output-dir {}/{}'.format(prokka_folder,gbk_list[file],
                                                                             output_folder,gbk_list[file])
        print(antismash)
        os.system(antismash)


def for_bigscape(folder_name):
    create_folder('for_bigscape')
    work_folder = 'antismash/{}'.format(folder_name)
    for file in os.listdir(work_folder):
        if file.endswith('.gbk') and file != folder_name:
            to_folder = '{}/for_bigscape/{}'.format(os.getcwd(), file)
            in_folder = '{}/antismash/{}/{}'.format(os.getcwd(), folder_name, file)
            with open(in_folder, 'r') as f_in:
                with open(to_folder, 'w') as f_out:
                    shutil.copyfileobj(f_in, f_out)
