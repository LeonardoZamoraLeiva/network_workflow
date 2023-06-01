# NetworkWorkflow
Complete workflow from genome download to BGC network visualization

## Instalation
pending....

## Acerca de esta herramienta
Esta herramienta es una tubería creada para facilitar los pasos necesarios para generar redes de BGC con BiG-SCAPE.
Es capaz de descargar 'n' genomas de RefSeq, evaluar su calidad, anotarlos, ejecutar antiSMASH y finalmente utilizar estos BGC para generar redes de BiG-SCAPE.
Cada paso se puede ejecutar de forma independiente, lo que la hace adecuada para necesidades específicas.

## Opciones disponibles
Opciones:
- -h, --help: muestra este mensaje de ayuda y sale
- -i file.csv, --input=file.csv: archivo CSV con cepas para descargar
- -o Carpeta, --out=Carpeta: carpeta de salida
- -d Visualización, --download=Visualización: permite la descarga desde la base de datos de RefSeq
- -q, --quality: determina la calidad de los genomas proporcionados
- -r Rango, --rank=Rango: rango para la comparación (género, familia, orden, clase, filo, reino, dominio)
- -t Taxon, --taxon=Taxon: por ejemplo, Streptomyces
- --completness=completness: completitud mínima aceptada para pasar la verificación de calidad
- --contigs=contig_number: número máximo de contigs aceptados para pasar la verificación de calidad
- --contamination=contamination: porcentaje máximo de contaminación aceptado para pasar la verificación de calidad
- -n anotación, --annotation=anotación: anota el genoma con el anotador asignado (prokka, dfast, etc.). Por defecto: prokka
- -a, --antismash: ejecuta antiSMASH
- -b, --bigscape: ejecuta BiG-SCAPE
- --bigscape_cutoffs=CUTOFF: umbrales para BiG-SCAPE. "0.3, 0.6, 0.9". Por defecto: 0.6
- -v, --visual: salida de visualización simple para BiG-SCAPE como un archivo HTML

## Mejoras futuras
- Hacerlo más rápido simplificando algunos análisis
- Agregar varios otros anotadores (como D-fast) como opciones
- Agregar visualización de características en el archivo de visualización



