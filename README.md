# NetworkWorkflow
Complete workflow from genome download to BGC network visualization

## Instalation
pending....

## About this tool
This tool is a pipeline created to facilitate the necessary steps for generating BGC networks with BiG-SCAPE. It is capable of downloading 'n' genomes from RefSeq, evaluating their quality, annotating them, running antiSMASH, and finally using these BGCs to generate BiG-SCAPE networks. Each step can be executed independently, making it suitable for specific needs.

## Available options

| Opción                         | Descripción                                                                                     |
|--------------------------------|-------------------------------------------------------------------------------------------------|
| -h, --help                     | Shows help message                                                            |
| -i file.csv, --input=file.csv  | input csv file with the strains or genera to download                                                           |
| -o folder, --out=folder      | Output folder                                                                               |
| -d download, --download=Download | Allows the download from RefSeq database                                 |
| -q, --quality                  | Allows the quality filter from checkM and Quast softwares                                              |
| -r Rank, --rank=rank         | Rank for comparison (genera, family, order, class, phylum, kingdom, domain)                  |
| -t Taxon, --taxon=Taxon        | For example, Streptomyces                                                                       |
| --completness=completness      | Minimum completeness to pass the quality filter                                |
| --contigs=contig_number        | Maximum contig number allow to pass the quality filter                        |
| --contamination=contamination  | Maximum contamination percentage to pass the quality filter               |
| -n annotation, --annotation=annotation | Allows the annotation with the assign software (prokka, dfast, etc.). Default: Prokka   |
| -a, --antismash                | Allows antiSMASH                                                                               |
| -b, --bigscape                 | Allows BiG-SCAPE                                                                               |
| --bigscape_cutoffs=CUTOFF      | BiG-SCAPE network cutoffs. "0.3, 0.6, 0.9". Por defecto: 0.6                                      |
| -v, --visual                   | Allows visualization from BiG-SCAPE output to an HTML file                              |

## Future improvements
- Enhance speed by simplifying some analyses
- Add several other annotators (such as D-fast) as options
- Incorporate feature visualization in the visualization file


