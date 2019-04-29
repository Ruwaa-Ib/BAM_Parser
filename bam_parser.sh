#!/bin/bash

work_dir="$(pwd)"
bam_file="$1"
output="$(basename -- $bam_file)"

samtools flagstat $bam_file > $output.flagstat

#------------------------------------------------------------
# 1- Extracting the required reads
mkdir parsed
# a) multiple mismatches 
	# m4 3arfa

# b) supplementary alignment
samtools view -h -f 2048 $bam_file > parsed/supp.$output

# c) discordant reads
samtools view -h -F 2 $bam_file > parsed/improper.$output

# d) reads with introns
samtools view -h 			> parsed/without_introns.$output
samtools view -h 			> parsed/with_introns.$output

#------------------------------------------------------------
# find the position of those reads
