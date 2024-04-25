# imports
import requests
import pandas as pd
from itertools import chain
from funct import *

# read and collect file type NC or NM
hgvs = pd.read_csv('hgvs.csv')
list_hgvs = hgvs.values.tolist()
linear_hgvs = list(chain.from_iterable(list_hgvs))

result = sort_values(linear_hgvs)
NC_list_mut, NG_list_mut, NM_list_mut, NP_list_mut = result[0], result[1], result[2], result[3]


# use the API question to get NM data
prefasta_name, prefasta_clear, prefasta_mut = [], [], []
for i in NM_list_mut:
    response = requests.get(f'https://mutalyzer.nl/api/normalize/{i}', timeout=100)
    json = response.json()
    data = json['protein']
    prefasta_name.append(data['description'])
    prefasta_clear.append(data['reference'])
    prefasta_mut.append(data['predicted'])


# use the API question to get NC data
name = []
prefasta_name_g, prefasta_clear_g, prefasta_mut_g = [], [], []

for i in NC_list_mut:
    response = requests.get(f'https://mutalyzer.nl/api/normalize/{i}', timeout=100)
    json = response.json()
    d = json['equivalent_descriptions']
    d = d['c']
    for k in d:
        name.append(k['description'])
    for g in name:
        response = requests.get(f'https://mutalyzer.nl/api/normalize/{g}', timeout=100)
        json_2 = response.json()
        data = json_2['protein']
        prefasta_name_g.append(data['description'])
        prefasta_clear_g.append(data['reference'])
        prefasta_mut_g.append(data['predicted'])


# create .fasta file for NM data
output_file = "clean.fasta"
write_fasta(prefasta_name, prefasta_clear, output_file)
output_file = "mutate.fasta"
write_fasta(prefasta_name, prefasta_mut, output_file)


NM_list_clear_f = add_clean_suffix(prefasta_name)
NM_list_mut_f = add_mut_suffix(prefasta_name)
NM_list_cl_and_mut = interleave_lists(NM_list_clear_f, NM_list_mut_f)
prefasta_cl_and_mut = interleave_lists(prefasta_clear, prefasta_mut)

output_file = "mutate_and_clean.fasta"
write_fasta(NM_list_cl_and_mut, prefasta_cl_and_mut, output_file)


# create .fasta file for NC data
output_file = "clean_g.fasta"
write_fasta(prefasta_name_g, prefasta_clear_g, output_file)
output_file = "mutate_g.fasta"
write_fasta(prefasta_name_g, prefasta_mut_g, output_file)

NM_list_clear_f = add_clean_suffix(prefasta_name_g)
NM_list_mut_f = add_mut_suffix(prefasta_name_g)
NM_list_cl_and_mut = interleave_lists(NM_list_clear_f, NM_list_mut_f)
prefasta_cl_and_mut = interleave_lists(prefasta_clear_g, prefasta_mut_g)

output_file = "mutate_and_clean_g.fasta"
write_fasta(NM_list_cl_and_mut, prefasta_cl_and_mut, output_file)
