import argparse 
from numpy import array
from numpy import *
from contig_function import * 

parser = argparse.ArgumentParser(description="")

parser.add_argument('-i', '--input',
					dest = 'input',
					action = 'store',
					default = None, 
					help = 'Input linear file with Contig information for each line')

parser.add_argument('-o', '--output',
					dest = 'output',
					action = 'store',
					default = None,
					help = 'Prefix for the two output files, one for the filtered results and another for the non-filtered.')

parser.add_argument('-hi', '--hits',
					dest = 'hits',
					action = 'store',
					type=float,
					default = 90,
					help = 'Minimum percent of eukaryotic hits required within a contig to be considered in the final cut')

parser.add_argument('-co', '--coverage',
					dest = 'coverage',
					action = 'store',
					type=float,
					default = 30,
					help = "Minimum percent of Exons' coverage required in a contig to be considered in the final cut")

options = parser.parse_args()

if __name__ == "__main__":

	if options.input is None:

		raise ValueError (">>> WARNING: Please, enter an input file to process. Write '-i (file)' <<<\n")

	else:
	
		infile = options.input


	if options.output is None:

		raise ValueError (">>> WARNING: Please, enter the prefix for the output files. Write '-o (prefix)' <<<\n")

	total_bp = 0

	filtered_bp = 0 

	fh2 = open(options.output+"_filtered.txt", 'w')

	fh3 = open(options.output+"_non_filtered.txt", 'w')

	for contig in contigs_info_generator(infile):

		cont_len = get_contig_len(contig)

		int_ex_cov = intron_exon_coverage(contig)

		euk_hits = get_euk_hits(contig)

		total_hits = euk_hits + get_bact_hits(contig) + get_virus_hits(contig) + get_arch_hits(contig)+ get_undef_hits(contig)

		if total_hits == 0:

			euk_ratio = 0

		else:

			euk_ratio = float(euk_hits) / total_hits

		total_bp += cont_len

		if int_ex_cov[1] >= float(options.coverage)/100 and euk_ratio >= float(options.hits)/100:

			filtered_bp += cont_len

			fh2.write("\t".join(contig)+"\n")

		else:

			pass

			fh3.write("\t".join(contig)+"\n")

	print "The total contigs' length that remained after the filtering is {0}.\nThe total contigs' length of the original file is {2}.\nWhich translates into a {1:.2%} from the original amount of contigs.\n".format(filtered_bp, float(filtered_bp)/total_bp, total_bp)