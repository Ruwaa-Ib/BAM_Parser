# importing libraries
import pysam
import re
import argparse

args = None

# ----------------------------------------------------------------------
def get_args():
	""""""
	parser = argparse.ArgumentParser(
		description="SplitN_RU - standalone tool that splits the reads with introns (contains 'N' in CIGAR string) in BAM/SAM file into distinct records that doesn't include introns.",
		epilog="Example:\npython SplitN_RU.py -I <input.bam> -O <output.bam>"
	)

	# required argument
	parser.add_argument('-I', action="store", required=True, help='Input alignment file (SAM/BAM).', metavar='<input.bam>')

	# optional arguments
	parser.add_argument('-O', action="store", help='Output file name.', default='output.bam', metavar='<output.bam>')

	arguments = vars(parser.parse_args())
	return arguments
# ----------------------------------------------------------------------


def consuming(record):
    ref_consume = 0
    seq_consume = 0
    cigar_lst = [i for i in record.cigar]
    # M I D N S H P = X B (NM)
    ref_lst = [0, 2, 3, 7, 8]
    seq_lst = [0, 1, 4, 7, 8]
    for tup in cigar_lst:
        if tup[0] in ref_lst:
        	ref_consume += tup[1]
        if tup[0] in seq_lst:
        	seq_consume += tup[1]
    return [ref_consume, seq_consume]
    

def main():
    # Loading the file
    bam = pysam.AlignmentFile(args['I'], 'rb') #"sorted_with_introns_SRR2973277.bam"
    output = pysam.AlignmentFile(args['O'], 'wb', template=bam) #"output.bam"

    # Loop over the records to process contigs
    for record in bam:
        # initialize
        seq = record.seq
        qual = record.qual
        original_cigar = record.cigarstring
        ref_pos = record.pos

        # splitting
        contigs = record.cigarstring.split('N') # contig by CIGAR
        contig_start = 0

        for contig in contigs:
            # prepare
            if contig[-1].isdigit():
                contig = contig + 'N'

            record.cigarstring = contig
            ref_consume, contig_len = consuming(record)

            if record.cigarstring[-1]=='N':
                record.cigarstring = re.sub(r'\d+$','',contig.rstrip('N'))

            # update
            record.seq = seq[contig_start:contig_start+contig_len]
            record.qual = qual[contig_start:contig_start+contig_len]
            record.pos = ref_pos
            if contig_start != 0 and record.flag < 2048:
                record.flag += 2048
            #record.cigarstring = contig
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

            # updating variables values
            ref_pos += ref_consume
            contig_start += contig_len
            
            
    bam.close()
    output.close()


# ----------------------------------------------------------------------
if __name__ == '__main__':
	args = get_args()
	main()

