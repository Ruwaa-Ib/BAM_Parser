# BAM Parser Bash Project

This tools is part of the Bioinformatics course project (ZC-BMS320)

Project Description >>  BAM parsing for assembly QC
>Parse BAM files to find the reads with multiple mismatches, supplementary alignment, and/or discordant reads. Try to find out if these reads aggregate in specific loci along the genome which might mark regions of bad assembly.

The Pipeline goes as follow:

### 1. Downloading and Indexing the Reference Human Genome
You should first create a new directory for this pipeline. Preferably, name it BAM_Parser.
```bash
work_dir="$(pwd)"

mkdir $work_dir/genome-data && cd $work_dir/genome-data

# download ref.
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.28_GRCh38.p13/GCA_000001405.28_GRCh38.p13_genomic.fna.gz

# unzipping
gunzip GCA_000001405.28_GRCh38.p13_genomic.fna.gz
ref_fna="$work_dir/genome-data/GCA_000001405.28_GRCh38.p13_genomic.fna"

# hisat indexing
mkdir idx
hisat2-build $ref_fna idx/grch38
index="$work_dir/genome-data/idx/grch38"

cd $work_dir
```

### 2. Downloading the sample of Interest from NCBI-SRA
```bash
fastq-dump -I --split-files $sample
```

### 3. Mapping the sample to the indexed reference human genome
```bash
mkdir map
hisat2 -q --phred33 \
	-x $index \
	-1 ${sample}_1.fastq \
	-2 ${sample}_2.fastq \
	-S map/$sample.sam \
	--met-file map/map.met \
	> map/map.log
```

### 4. Converting SAM to BAM
```bash
samtools view -hbo $sample.bam map/$sample.sam 
```

### 5. Extracting Records from the BAM file for two Different Purposes
All the above steps were done for to create the BAM files where the real project comes in. 
The first purpose is to select the reads with intronic sequences, split them over the introns, merge them with all other mapped reads. 
The second purpose was to use the mapped reads to assess the quality control of the reference assembly (or the sample of interest) based on three different criteria: proper alignments of paired end reads, chimeric (supplementary) alignments, and the accumulation of multiple mismatches at specific loci of the refernce genome.

The following code was done for enviroenment prep. but each subtask later was done by a different individual as mentioned.

```bash
mkdir parsed
bam_file="$sample.bam"
output="$(basename -- $bam_file)"
```

#### a) Purpose 1: getting the records with intronic sequences (CIGAR)  >> Ruwaa
```bash
mkdir introns
samtools view -h -F 4 $bam_file | awk '$6 !~ /N/ || $1 ~ /@/' | samtools view -b > introns/without_introns_$output
samtools view -h -F 4 $bam_file | awk '$6 ~ /N/ || $1 ~ /@/' | samtools view -b > introns/with_introns_$output


# split the recrods in the introns file to exons (without introns)
cd introns/
bam_file="with_introns_SRR2973277.bam"

# sorting
samtools view -H parsed/$bam_file > parsed/header.bam
samtools sort -o parsed/sorted_$bam_file parsed/$bam_file

# 1) using SplitNCigarReads
conda activate ngs
gatk SplitNCigarReads -R $fna_file -I parsed/sorted_$bam_file -O parsed/Split_N.bam

# 2) using my Python script
python SplitN_RU.py -b bam_file -o splitted_RU.bam


# counting lines and comparing (benchmarking)
samtools view parsed/sorted_$bam_file | wc -l
samtools view parsed/Split_N.bam | wc -l
samtools view parsed/splitted_RU.bam | wc -l

```
When using the SplitNCigarReads tools of GATK >> when viewd, some records still contan introns 'N' in the CIGAR string! A new python/bash script is needed for the splitting.

When using my Python script >> 


#### b) Purpose 2: getting the records that made improper alignment (F)  >> Amira
```bash
samtools view -h -F 2 $bam_file > parsed/improper_$output
```

#### c) Purpose 3: getting the records with supplementary alignment (F)  >> Negm
```bash
samtools view -h -f 2048 $bam_file > parsed/supp_$output
```

#### d) Purpose 4: getting the records with multiple mismatch (Flags)  >> Mayar
```bash
samtools view -h -F 4 $bam_file | #...
```
there are two options here:
 1. SamFixCigar (tool >> http://lindenb.github.io/jvarkit/)
 2. there is a tag named MD that can be used for that purpose!
 
 I support the second option. See this tutorial >> http://zenfractal.com/2013/06/19/playing-with-matches/

