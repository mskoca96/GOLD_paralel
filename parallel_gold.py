#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def split_ligands_files(ligands_path, cpu_number):
        lig_files = os.listdir(ligands_path)
        sep_files = list(split(lig_files, cpu_number))
        return sep_files


def create_output_files(sep_files):
    os.system("mkdir output")



def sub_conf_jobs(conf_file):
    f = open(conf_file,"r")
    file_conf = []
    for line in f:
        file_conf.append(line)
    index = file_conf.index("  DATA FILES\n")
    part_1 = file_conf[0:index+1]
    index = file_conf.index("tordist_file = DEFAULT\n")
    part_2 = file_conf[index:-1]
    return part_1, part_2



def main(ligands_path, cpu_number, conf_file, pose_number):
    sep_files = split_ligands_files(ligands_path,cpu_number)
    create_output_files(sep_files)
    part_1 = sub_conf_jobs(conf_file)[0]
    part_2 = sub_conf_jobs(conf_file)[1]
    for i in range(0,len(sep_files)):
        txt_file = open("./gold_%d.conf"%i, "w")
        for element in part_1:
            txt_file.write(element)
        for element in sep_files[i]:
            txt_file.write("ligand_data_file "+ligands_path+ element+ " "+pose_number+"\n")
        txt_file.write("param_file = DEFAULT\n")
        txt_file.write("set_ligand_atom_types = 1\n")
        txt_file.write("set_protein_atom_types = 0\n")
        txt_file.write("directory = ./output/%d"%i+"\n")
        for element in part_2:
            txt_file.write(element)
        os.system("gold_auto gold_%d.conf & "%i)

main("./ligands",4,"gold.conf","10")


