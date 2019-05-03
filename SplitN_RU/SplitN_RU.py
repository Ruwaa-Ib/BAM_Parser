# importing libraries
import pysam
import re

# Loading the file
bam = pysam.AlignmentFile("sorted_with_introns_SRR2973277.bam", 'rb')
output = pysam.AlignmentFile("output.bam", 'wb', template=bam)

# Loop over the records to process contigs
for record in bam:
    # initialize
    seq = record.seq
    qual = record.qual
    #length = record.query_length
    ref_pos = record.pos
    
    # splitting
    contigs = record.cigarstring.split('N') # contig by CIGAR
    contig_start = 0

    for contig in contigs:
    	# prepare
    	ref_consume = sum(int(i) for i in re.split(r'[^\d]', contig) if i.isdigit())
    	
    	if contig[-1] == 'D':
    		contig = re.sub(r'\d+$','',contig.rstrip('D'))
    	contig_len = sum(int(i) for i in re.split(r'[^\d]', contig) if i.isdigit())
    	
    	# update
    	record.seq = seq[contig_start:contig_start+contig_len]
    	record.qual = qual[contig_start:contig_start+contig_len]
    	record.pos = ref_pos
    	record.cigarstring = contig
    	record.tags = []
    	#### tags!!!! (NM: edit distance), (MD: String for mismatching positions), (NH: Number of reported alignments that contain the query in the current record), (MC: CIGAR string for mate/next segment)
#    	for tag in record.tags:
#    		tag = list(tag)
#    	    if tag[0]=='NM':
#    	        pass
#    	    elif tag[0]=='MD':
#    	        pass
#    	    elif tag[0]=='NH':
#    	    	tag[1] += 1
#    	    tag = tuple(tag)
    	
    	# write to the new file
    	output.write(record)
    	
    	# prepare for the next
    	ref_pos += ref_consume
    	contig_start += contig_len
    	
#    break
    	
bam.close()
output.close()
