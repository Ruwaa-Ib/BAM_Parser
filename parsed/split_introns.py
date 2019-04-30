# spliting BAM records at interons

import pysam
import re

bam = pysam.AlignmentFile("sorted_with_introns_SRR2973277.bam")
bam_header = bam.header # not string
for record in bam:
    print(record)
    contigs_lst = record.cigarstring.split('N')
##    contig_lst = re.split(r'\d*N', record.cigarstring)
##    length_lst = re.split(r'[^\d]', record.cigarstring)[:-1]
##    total_len = sum(int(i) for i in length_lst if i.isdigit())
##    total_introns_len = total_len - record.query_length
    new_recods_start = []
    start = record.pos
    contig_start = 0
    for contig in contigs_lst:
        # pos of contig = start
        new_recods_start.append(start)
        length_lst = re.split(r'[^\d]', contig)
        new_contig_len = sum(int(i) for i in length_lst if i.isdigit())
        # seq of contig = record.seq[contig_start:contig_start+new_contig_len]
        # qual of contig =record.qual[]
        # cigar_string = re.sub(r'\d+$','',contig)
        # write line >> record replace the seq, quality, pos, and cigar
        start += new_contig_len
        # contig_start += new_contig_len
        break
    break



## we can use record.cigartuples instead >> (type, number)
## OR record.get_blocks() >> returns gapless blocks (introns and insertions!) l2 m4 hatnf3.
