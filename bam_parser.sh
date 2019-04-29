#!/bin/bash

work_dir="$(pwd)"
bam_file="$1"
output="$(basename -- $bam_file)"

samtools flagstat $bam_file > $output.flagstat

#------------------------------------------------------------
# 1- Extracting the required reads
mkdir parsed
# a) multiple mismatches 
samtools view -h -F 4 $bam_file | #...
# there are twi options here:
	# 1- SamFixCigar 
	# 2- there is a tag named MD that can be used for that purpose!


# b) supplementary alignment
samtools view -h -f 2048 $bam_file > parsed/supp.$output


# c) discordant reads
samtools view -h -F 2 $bam_file > parsed/improper.$output


# d) reads with introns
samtools view -h -F 4 $bam_file | awk '$6 !~ /N/ || $1 ~ /@/' | samtools view -b > parsed/without_introns_$output
samtools view -h -F 4 $bam_file | awk '$6 ~ /N/ || $1 ~ /@/' | samtools view -b > parsed/with_introns_$output


