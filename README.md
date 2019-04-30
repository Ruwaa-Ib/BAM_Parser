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
hisat2 -q --phred33 \
	-x $index \
	-1 $sample_1.fastq \
	-2 $sample_2.fastq \
	-S $sample.sam \
	--met-file map.met \
	> map.log
```

### 4. Converting SAM to BAM
```bash
samtools view -hbo $sample.bam $sample.sam 
```

### 5. Extracting Records from the BAM file for Different Purposes
Insert some description here!
```bash
mkdir parsed
```

#### a) Purpose 1: getting the records with intronic sequences (CIGAR)
```bash
samtools view -h -F 4 $bam_file | awk '$6 !~ /N/ || $1 ~ /@/' | samtools view -b > parsed/without_introns_$output
samtools view -h -F 4 $bam_file | awk '$6 ~ /N/ || $1 ~ /@/' | samtools view -b > parsed/with_introns_$output
```

#### b) Purpose 2: getting the records that made improper alignment (F)
```bash
samtools view -h -F 2 $bam_file > parsed/improper.$output
```

#### c) Purpose 3: getting the records with supplementary alignment (F)
```bash
samtools view -h -f 2048 $bam_file > parsed/supp.$output
```

#### d) Purpose 4: getting the records with multiple mismatch (CIGAR)
```bash
samtools view -h -F 4 $bam_file | #...
```
there are two options here:
 1. SamFixCigar (tool >> http://lindenb.github.io/jvarkit/)
 2. there is a tag named MD that can be used for that purpose!
 
 I support the second option. See this tutorial >> http://zenfractal.com/2013/06/19/playing-with-matches/

