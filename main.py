import os
from optparse import OptionParser
from ftplib import FTP
from ftp_conection import download_file
from unzip import new_unzip_func
from checkm import checkm_command, filter_strains, quast_quality,merge_quality_checkM_quast
from prokka import prokkafunc
from antismash import antismash_func, for_bigscape
from bigscape_script import bigscape_func, modify_output
from network import network_visualization_func
from move_rename import create_folder
import pandas as pd
from domains import from_json_extract_files, create_faa_from_gbk, antismash_json_compare
#import requests
import json
import csv


def main():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', help='Csv file with strains to dowload',metavar='file.csv')
    parser.add_option('-o', '--out', dest='output', help='Output folder', metavar='Folder')
    parser.add_option('-d', '--download', dest='download', help='Allows the download from refseq database', metavar='Visualization')

    parser.add_option('-q', '--quality', dest='quality', help='determine quality of given genomes', action='store_true')
    parser.add_option('-r', '--rank', dest='rank', help='rank for comparison (genus, family, order, class, phylum, kingdom, domain', metavar='Rank')
    parser.add_option('-t', '--taxon', dest='taxon', help='eg. Streptomyces', metavar='Taxon')
    parser.add_option('--completness', dest='completness', default=98,
                      help='Minimun completness accepted to pass the quality check', metavar='completness')
    parser.add_option('--contigs', dest='contigs', default=200, help='Maximum contig number accepted to pass the quality check',
                      metavar='contig_number')
    parser.add_option('--contamination', dest='contamination', default=5,
                      help='Maximum contamination percentage accepted to pass the quality check', metavar='contamination')
    parser.add_option('-n', '--annotation', dest='annotation', default='prokka', help='annotate the genome with the assigned annotator (prokka,dfast,etc). Default = prokka', metavar='annotation')
    parser.add_option('-a', '--antismash', action='store_true', dest='antismash', help='do antismash')
    parser.add_option('-b', '--bigscape', action='store_true', dest='bigscape', help='do bigscape')
    parser.add_option('--bigscape_cutoffs', dest='cutoff', default='0.6', help='cutoffs for bigscape. "0.3, 0.6, 0.9" Default = 0.6', metavar=None)
    parser.add_option('-v', '--visual', dest='visualization', action='store_true', help='Simple visualization output for bigscape run', metavar='Visualization')

    (options,args) = parser.parse_args()

    def intersection(lst1, lst2):
        lst3 = []
        for i in range(len(lst1)):
            for j in range(len(lst2)):
                if lst1[i] in lst2[j] and lst2[j] not in lst3:
                    lst3.append(lst2[j])
        return lst3

    # all folders needed for the run
    strain_of_analysis = options.output
    project_folder = '{}/{}'.format(os.getcwd(), strain_of_analysis)
    download_folder = '{}/zip_for_{}'.format(project_folder, strain_of_analysis)
    unzip_folder = '{}/unzip_for_{}'.format(project_folder, strain_of_analysis)
    checkm_folder = '{}/checkm'.format(unzip_folder)
    prokka_results_folder = '{}/prokka_{}'.format(project_folder, strain_of_analysis)
    prokka_gbks_folder = '{}/prokka_gbks_{}'.format(project_folder, strain_of_analysis)
    antismash_folder = '{}/antismash_for_{}'.format(project_folder, strain_of_analysis)
    for_bigscape_folder = '{}/for_bigscape_{}'.format(project_folder, strain_of_analysis)
    bigscape_output_folder = '{}/bigscape_results'.format(project_folder)
    cutoffs = options.cutoff


    if options.download:
        ###          Extract files from ncbi.refseq ftp         #####
        host_address = 'ftp.ncbi.nlm.nih.gov'
        user_name = 'anonymous'
        password = 'leo.zamoraleiva@gmail.com'
        ftp = FTP(host_address)
        ftp.login(user=user_name, passwd=password)

        # opening the file in read mode
        my_file = open(options.input, "r")
        # reading the file
        data = my_file.read()

        # replacing end of line('/n') with ' ' and
        # splitting the text it further when '.' is seen.
        strainCollection = data.replace('\n', ' ').split(' ')
        strepto_ftp = []
        # printing the data
        print(strainCollection)
        my_file.close()

        for j in range(len(strainCollection)):
            print('Nos estamos conectando a refseq')
            for i in ftp.nlst('genomes/refseq/bacteria'):
                if strainCollection[j] in i:
                    strepto_list = i.split(sep='/')
                    strepto_ftp.append(strepto_list[-1])
            ftp.close()
        print(strainCollection)
        print(len(strepto_ftp))
        # here it hast to interset either list that is used as input: strainCollection or strain_list
        list_interc = intersection(strainCollection, strepto_ftp)

        print('Vamos a descargar {} especies distintas'.format(len(list_interc)))

        create_folder(download_folder)
        for n in strepto_ftp:
            ftp = FTP(host_address)
            ftp.login(user=user_name, passwd=password)
            all_strains_list = ftp.nlst('genomes/refseq/bacteria/{}'.format(n))
            for i in all_strains_list:
                count = 0
                if 'genomes/refseq/bacteria/{}/latest_assembly_versions'.format(n) in i:
                    download_file(download_folder, n)
                    count = count + 1
                    ftp.close()
                    if count == len(all_strains_list):
                        break

    # Unzip donwloaded files, analyze qualtity and filter
    #Unzip and move files
    create_folder(unzip_folder)
    new_unzip_func(download_folder, unzip_folder, strain_of_analysis)

    #checkM and quast quality test. Also merge them on a single file
    strains_that_pass = ''
    if options.quality:
        if options.taxon and options.rank:
            taxon = options.taxon
            rank = options.rank
            checkm_command(unzip_folder, checkm_folder, rank, taxon)
            quast_quality(unzip_folder)
            merge_quality_checkM_quast(unzip_folder, strain_of_analysis, taxon)
            # filter strains that pass the quality tests
            strains_that_pass = filter_strains(strain_of_analysis, options.contigs, options.completness, options.contamination)
            print('{} strains pass the quality check'.format(len(strains_that_pass)))
        else:
            print('Taxon and rank are needed for quality analysis with checkM')

    # Prokka annotation
    if options.annotation:
        if prokka_results_folder not in os.listdir():
            create_folder(prokka_results_folder)
        for strain in strains_that_pass:
            try:
                prokkafunc(strain, unzip_folder, prokka_results_folder, prokka_gbks_folder)
            except ValueError:
                print("{} can't be annotated".format(strain))
    
    # antiSMASH analysis
        create_folder(antismash_folder)
        antismash_func(prokka_gbks_folder, antismash_folder)

    '''
    ###          domains addition         #####
    ###     Obtain json file from PRISM page
    strain = 'G11C_PacBio_Illumina_Flye_Pilon_09102020'
    json_file = requests.get('https://prism.adapsyn.com/api/task/8325cbce7827fa01ade350e14f34bbc1/results/file')
    all_file = json.loads(json_file.text)
    
    ###  Extract sequence files from PRISM json file and the to_search_dict 
    to_search_dict = from_json_extract_files(all_file,strain)
    
    ### Create fasta files to compare with diamond
    number_domain_dict = {}
    count = 0
    for key in to_search_dict:
        count += 1
        with open('G11C/sequences/{}.fasta'.format(count), 'w') as f:
            f.write('>{}\n{}'.format(count, key))
            number_domain_dict[count] = to_search_dict[key]
    
    print(number_domain_dict)
    
    ### Create faa from antismash gbk to usen on diamond
    #antismash_dir = 'G11C/antismash_for_G11C/'
    
    for file in os.listdir(antismash_folder):
        if file.endswith('.gbk'):
            gbk_filename = '{}/{}'.format(antismash_folder, file)
            faa_filename = '{}/{}.faa'.format(antismash_folder, file[0:-4])
            create_faa_from_gbk(gbk_filename, faa_filename)
    
    ### Compare sequences from json with antismash to find hits and create output
    sequences_to_compare_folder = 'G11C/sequences'
    output_folder_diamond = 'G11C/results_diamond'
    antismash_json_compare(antismash_folder, sequences_to_compare_folder, output_folder_diamond)
    
    files_dict = {}
    for result in os.listdir('G11C/results_diamond'):
        key_lists = list(number_domain_dict.values())
        key = int(result.split('_')[0])
        if result.split('_', 1)[1][0:-4] not in list(files_dict.keys()):
            files_dict[result.split('_', 1)[1][0:-4]] = number_domain_dict[key]
        else:
            files_dict[result.split('_', 1)[1][0:-4]].append(number_domain_dict[key])
    
    print(files_dict)
    
    header = ['Source', 'Domains']
    with open('G11C/domains.csv', 'w') as f:
        file_writter = csv.writer(f, delimiter= ',')
        file_writter.writerow(header)
        for key, value in files_dict.items():
            file_writter.writerow([key, value])
    
    '''
    # bigscape run
    if options.bigscape:
        for folder in os.listdir(antismash_folder):
            for_bigscape(folder, for_bigscape_folder, antismash_folder)
            bigscape_func(for_bigscape_folder, bigscape_output_folder, cutoffs)
            modify_output(bigscape_output_folder, 'domains.csv')
            modify_output(bigscape_output_folder)

    
    # Network visualization
    if options.visualization:
        network_folder = '{}/network_files'.format(bigscape_output_folder)
        for folder, subfolder, files in os.walk(network_folder):
            for i in range(len(subfolder)):
                if "hybrids" not in subfolder[i] and 'transformed' in subfolder[i]:
                    subfolder_full = '{}/{}'.format(network_folder, subfolder[i])
                    for file in os.listdir(subfolder_full):
                        if file.endswith('edges.csv'):
                            file_full_path = '{}/{}'.format(subfolder_full, file)
                            network_visualization_func(file_full_path)

if __name__ == '__main__':
    main()
