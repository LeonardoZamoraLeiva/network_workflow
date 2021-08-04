import os
from move_rename import move_rename, create_folder


def prokkafunc(strain, from_folder,prokka_out,prokka_gbks):
    create_folder(prokka_gbks)
    create_folder(prokka_out)
    strain_full = '{}.fna'.format(strain)
    if strain_full in os.listdir(from_folder):
        output_folder = '{}/{}/{}/'.format(os.getcwd(), 'prokka_out', strain)
        input_file = '{}/{}'.format(from_folder, strain_full)
        prokka = 'prokka --outdir {} {}'.format(output_folder, input_file)
        print(prokka)
        os.system(prokka)
        to_folder = '{}/prokka_gbks/{}.gbk'.format(os.getcwd(), strain)
        move_rename(output_folder, to_folder)
