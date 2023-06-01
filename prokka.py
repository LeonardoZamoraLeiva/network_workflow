import os
from move_rename import move_rename, create_folder


def prokkafunc(strain, from_folder,prokka_out,prokka_gbks):
    strain_full = '{}.fna'.format(strain)
    output_folder = '{}/{}/'.format(prokka_out, strain)
    input_file = '{}/{}'.format(from_folder, strain_full)
    if strain not in os.listdir(prokka_out):
        create_folder(prokka_out)
        if strain_full in os.listdir(from_folder):
            prokka = 'prokka --cpus 0 --outdir {} {}'.format(output_folder, input_file)
            print(prokka)
            os.system(prokka)
            create_folder(prokka_gbks)
            to_folder = '{}/{}.gbk'.format(prokka_gbks, strain)
            move_rename(output_folder, to_folder)
