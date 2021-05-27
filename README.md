# network_workflow
Complete workflow from genome download to BGC network visualization
## Meetings journal
### Reunión 25/May/2021

* Revision de todo el workflow del analisis de creacion de redes de similitud de agrupaciones geneticas biosinteticas (BCGs) desde genomas descargados de RefSeq.
*  Paso 1: Descargar desde genomas (###.fna) de bacterias FTP "Streptomyces"
*  Paso 2: Verificar calidad de genomas usando CheckM
*  Paso 3: Anotacion parcial de ###.fna para obtener ###.gbk (sin comparacion a bases de datos)
*  Paso 4: Anotacion mediante Antismash v.5.2 para obtener ####.gbk de cada genoma descargado
*  Paso 5: Creacion de redes de similitud mediante BigSCAPE v.1.0.2 para obtener archivos nodes.csv y edges.csv
*  Paso 6: Visualizacion mediante programa no tan bueno como Gephi

Mejoras pendientes:
* -Incluir CheckM al workflow
* -Identificar taxonomicamente phylum:class:order:family:genus:species de cada genero y especie para darle el taxon superior a checkM
* -Contar ">" para filtro de numero de contigs
* -Anotacion parcial, solo realizar hasta identificacion de CDS, no comparar con bases de datos
* -Antismash agregar workflow basico (solo .gbk) o completo ClusterBlast visualizacion del index.html
* -Agregar visualizador de nodes.cdv y edges.csv

#### Tareas
* Leonardo:  CheckM script para llamarlo, activar por pasos el workflow
* Roberto: buscar csv/tsv taxonomia y anotacion parcial


27-05-21
Leonardo: Code upload -- Done --
