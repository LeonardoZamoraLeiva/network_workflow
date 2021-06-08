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

### Reunion 08/Jun/2021
Revision de tareas pendientes:
Leo: Instaló CheckM v.1.1.3, se realizo por Conda ya que un programa no se podia instalar. El workflow usado es el taxonomywf (dar Rank:"genus" y name: Streptomyces), output da un archivo ########.ms y luego se utiliza como input para el workflow qa. Esto genera una tabla, que se filtra mediante la funcion "filter_strains" utiliza completeness, contamination, and N° contigs. Esto genera una lista que guarda el valor "Bin ID", nombre del archivo .fna.
Se agregó error handling (try ... except) para que el programa siga aunque encuentre un error.
Error con scikitlearn: numpy... el error no es un error real, future_error
El output de bigscape se transforma en una version ms legible para pyvis.network 
Se creo la funcion que crea la visualizacion de los nodes. pyvis.network (library).

Roberto: Incorporar taxonkit, instalar DFAST de forma manual y usar --no_func_anno para anotar sin comparar en bases de datos. 


####Tareas pendientes: 
Leo: Incorporar taxonkit para FTP-download y checkM. DFAST  --no_func_anno
Activacion de lineas de comandos.
Potential new clusters for BCGs (non reported) y tiene posee genes interesanes seria bueno incluirlo.
Realizar archivo de reportes (incluir errores del programa)
Exportar imagen desde pyvys.network como pdf, svg, png..
Pendiente estandarizar nombre archivo.fna y contigs para output de visualizacion de nodos y normalizar nombres de carpetas.
Separar carpetas de BigScape para clasificar por tipo de BCG

Roberto: Ver todo lo asociado a .html (agregar info de gbk. de antismash en el html de cada nodes, para visualizacion online)
Antismash libera un html con un index que te lleva al BCG de la pagina de antismash. html de Bigscape 4.9 kb pasa a 48 kb.
Cuanto se demoro la corrida, cuales parametros usaste, BCGs per genome, BCG per clade. 

### Proxima Reunion 22/Jun/2021
