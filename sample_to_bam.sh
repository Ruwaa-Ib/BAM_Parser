#!/bin/bash

work_dir="$(pwd)"
sample="$1"

#------------------------------------------------------------
# 1- Downloading and Indexing the reference
index=$(bash ref_prep.sh "$work_dir")

#------------------------------------------------------------
# 2- Download the sample from SRA
fastq-dump -I --split-files $sample 2> fastq-dump.log

#------------------------------------------------------------
# 3- mapping the sample
hisat2 -q --phred33 \
	-x $index \
	-1 $sample_1.fastq \
	-2 $sample_2.fastq 
	-S $sample.sam \
	--met-file map.met \
	> map.log

#------------------------------------------------------------
# 4- Convert SAM to BAM
samtools view -hbo $sample.bam $sample.sam 


#------------------------------------------------------------
# 5- BAM parser calling
bash bam_parser.sh "$sample.bam"
