# NetworkWorkflow
Complete workflow from genome download to BGC network visualization
## Instalation
pending....
##About this tool
This tool is a pipeline created to facilitate the steps that are needed to generate BGC networks with BiG-SCAPE.
It is capable of download 'n' genomes from refseq, evaluate their quality, annotate them, run antiSMASH on them and finnaly uses this BGCs to generate BiG-SCAPE networks.
Can run every step independently, so can be uses for specific needs.

##Available options
Options:
  -h, --help            show this help message and exit
  -i file.csv, --input=file.csv
                        Csv file with strains to dowload
  -o Folder, --out=Folder
                        Output folder
  -d Visualization, --download=Visualization
                        Allows the download from refseq database
  -q, --quality         determine quality of given genomes
  -r Rank, --rank=Rank  rank for comparison (genus, family, order, class,
                        phylum, kingdom, domain
  -t Taxon, --taxon=Taxon
                        eg. Streptomyces
  --completness=completness
                        Minimun completness accepted to pass the quality check
  --contigs=contig_number
                        Maximum contig number accepted to pass the quality
                        check
  --contamination=contamination
                        Maximum contamination percentage accepted to pass the
                        quality check
  -n annotation, --annotation=annotation
                        annotate the genome with the assigned annotator
                        (prokka,dfast,etc). Default = prokka
  -a, --antismash       do antismash
  -b, --bigscape        do bigscape
  --bigscape_cutoffs=CUTOFF
                        cutoffs for bigscape. "0.3, 0.6, 0.9" Default = 0.6
  -v, --visual          Simple visualization output for bigscape run as an HTML file


##Future improvements
- Make it faster by simplifying some analysis 
- Addition several other annotators (like D-fast) as options
- Add feature display on the visualization file
- 



