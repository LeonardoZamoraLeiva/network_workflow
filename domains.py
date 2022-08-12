from Bio import SeqIO
import os
import json
import requests


def diamond_func(query_fasta, faa_file, output_file):
    # create_folder(output_folder)
    os.system(
        'diamond blastp --quiet --id 90 --query-cover 95 -d {} -q {} -o {}'
            .format(query_fasta, faa_file, output_file))


def from_json_extract_files(prism_report,strain):
    to_search_dict = {}
    if strain in prism_report['prism_results']['input']['filename']:
        to_search_init = prism_report['prism_results']['clusters']
        count = 0
        for i in range(len(to_search_init)):
            for j in range(len(to_search_init[i]['orfs'])):
                try:
                    if len(to_search_init[i]['orfs'][j]['domains']) > 0:
                        domains_list = []
                        for d in range(len(to_search_init[i]['orfs'][j]['domains'])):
                            domains_list.append(to_search_init[i]['orfs'][j]['domains'][d]['clean_name'])
                            to_search_dict[to_search_init[i]['orfs'][j]['sequence']] = domains_list
                except:
                    print ('doesnt exist')
    return to_search_dict


def create_faa_from_gbk(gbk_filename,faa_filename):
    input_handle  = open(gbk_filename, 'r')
    output_handle = open(faa_filename, 'w')
    #print (input_handle)
    for seq_record in SeqIO.parse(input_handle, 'genbank'):
        print ("Dealing with GenBank record %s"% seq_record.id)
        for seq_feature in seq_record.features :
            if seq_feature.type=="CDS" :
                assert len(seq_feature.qualifiers['translation'])==1
                output_handle.write(">%s from %s\n%s\n" % (
                       seq_feature.qualifiers['locus_tag'][0],
                       seq_record.name,
                       seq_feature.qualifiers['translation'][0]))
    output_handle.close()
    input_handle.close()


def antismash_json_compare(antismash_folder, sequences_to_compare_folder, output_folder):
    for faa in os.listdir(antismash_folder):
        if faa.endswith('faa'):
            for sequence in os.listdir(sequences_to_compare_folder):
                faa_path = '{}/{}'.format(antismash_folder, faa)
                sequence_path = '{}/{}'.format(sequences_to_compare_folder, sequence)
                out_file = '{}_{}.tsv'.format(sequence[0:-6], faa[0:-4])
                print (out_file)
                diamond_func(sequence_path, faa_path, '{}/{}'.format(output_folder, out_file))
                if os.stat('{}/{}'.format(output_folder, out_file)).st_size==0:
                    os.remove('{}/{}'.format(output_folder, out_file))