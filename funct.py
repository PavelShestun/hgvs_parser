# Sorting by individual terms
def sort_values(input_list):
    NC_list, NG_list, NM_list, NP_list = [], [], [], []

    for value in input_list:
        if value.startswith("NC"):
            NC_list.append(value)
        elif value.startswith("NG"):
            NG_list.append(value)
        elif value.startswith("NM"):
            NM_list.append(value)
        elif value.startswith("NP"):
            NP_list.append(value)

    return NC_list, NG_list, NM_list, NP_list


# Recording in fasta format from 2 lists
def write_fasta(file_names, sequences, output_file):
    with open(output_file, "w") as f:
        for name, sequence in zip(file_names, sequences):
            f.write(">" + name + "\n")
            f.write(sequence + "\n")


# Adding a label to each value
def add_clean_suffix(input_list):
    cleaned_list = [item + " clean" for item in input_list]
    return cleaned_list


def add_mut_suffix(input_list):
    cleaned_list = [item + " mutate" for item in input_list]
    return cleaned_list


# alternation in the list
def interleave_lists(list_a, list_b):
    interleaved_list = []
    min_length = min(len(list_a), len(list_b))

    for i in range(min_length):
        interleaved_list.append(list_a[i])
        interleaved_list.append(list_b[i])

    if len(list_a) > min_length:
        interleaved_list.extend(list_a[min_length:])
    elif len(list_b) > min_length:
        interleaved_list.extend(list_b[min_length:])

    return interleaved_list