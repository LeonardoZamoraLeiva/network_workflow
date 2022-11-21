# NetworkWorkflow
Complete workflow from genome download to BGC network visualization
## Instalation
pending....
## About this tool
This tool is a pipeline created to facilitate the steps that are needed to generate BGC networks with BiG-SCAPE.<br>
It is capable of download 'n' genomes from refseq, evaluate their quality, annotate them, run antiSMASH on them and finnaly uses this BGCs to generate BiG-SCAPE networks.<br>
Can run every step independently, so can be uses for specific needs.

## Available options
Options: <br>
-h, --help -------------------------------------- show this help message and exit</br>
  -i file.csv, --input=file.csv --------------------- Csv file with strains to dowload<br>
  -o Folder, --out=Folder ----------------------- Output folder<br>
  -d Visualization, --download=Visualization -- Allows the download from refseq database<br>
  -q, --quality -------------------------------- Determine quality of given genomes<br>
  -r Rank, --rank=Rank ------------------------- Rank for comparison (genus, family, order, class, phylum, kingdom, domain<br>
  -t Taxon, --taxon=Taxon ---------------------- eg. Streptomyces<br>
  --completness=completness -------------------- Minimun completness accepted to pass the quality check<br>
  --contigs=contig_number ---------------------- Maximum contig number accepted to pass the quality check<br>
  --contamination=contamination ---------------- Maximum contamination percentage accepted to pass the quality check<br>
  -n annotation, --annotation=annotation ------- Annotate the genome with the assigned annotator (prokka,dfast,etc). Default = prokka<br>
  -a, --antismash ------------------------------ Do antismash<br>
  -b, --bigscape ------------------------------- Do bigscape<br>
  --bigscape_cutoffs=CUTOFF -------------------- Dutoffs for bigscape. "0.3, 0.6, 0.9" Default = 0.6<br>
  -v, --visual --------------------------------- Simple visualization output for bigscape run as an HTML file<br>


## Future improvements
- Make it faster by simplifying some analysis <br>
- Addition several other annotators (like D-fast) as options<br>
- Add feature display on the visualization file<br>
- 



