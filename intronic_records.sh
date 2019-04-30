#!/bin/bash

#work_dir="$(pwd)"
bam_file="with_introns_SRR2973277.bam"
work_dir="~/Documents/ZewailCity/19_Spring/BMS320_Bioinformatics/BAM_Parser"
fna_file="$work_dir/genome-data/GCA_000001405.28_GRCh38.p13_genomic.fna"

samtools view -H parsed/$bam_file > parsed/header.bam

samtools sort -o parsed/sorted_$bam_file parsed/$bam_file


gatk SplitNCigarReads -R $fna_file -I parsed/sorted_$bam_file -O parsed/Split_N.bam




fna_file="genome-data/GCA_000001405.28_GRCh38.p13_genomic.fna"
