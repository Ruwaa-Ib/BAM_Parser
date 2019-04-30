# Influenza A virus

### 1. Preparing the Reference Genome
```bash
work_dir="$(pwd)"

# create a directory for the refrence
mkdir $work_dir/genome-data && cd $work_dir/genome-data

# download ref. genome
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/865/085/GCF_000865085.1_ViralMultiSegProj15622/GCF_000865085.1_ViralMultiSegProj15622_genomic.fna.gz

# unzipping
gunzip GCF_000865085.1_ViralMultiSegProj15622_genomic.fna.gz 
ref_fna="$work_dir/genome-data/GCF_000865085.1_ViralMultiSegProj15622_genomic.fna"

# indexing
mkdir idx
hisat2-build $ref_fna idx/GCF
index="$work_dir/genome-data/idx/GCF"

cd $work_dir
```

### 2. Downloading the sample of interest
```bash
sample="SRR8910240"
fastq-dump -I --split-files $sample
```

### 3. Mapping to the indexed reference genome
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
