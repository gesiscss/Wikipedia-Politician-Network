# Temporal Network of Politicians on Wikipedia

## Dataset

The dataset with additional information about it is available on the following adress: https://datorium.gesis.org/xmlui/handle/10.7802/1515

The data used for this project is located in the politician-data-wikipedia-edge-list.zip file, which contains: 
* Edge list files - containing edges between politician pages on Wikipedia through time
* Politician data - data about the politicians that can be found on Wikipedia

## Dataset Augmentations

### Gender

As all the politicians from the original dataset (described above) do not have gender specified, gender inference was performed based on the method proposed in this paper ["Inferring Gender from Names on the Web: A Comparative Evaluation of Gender Detection Methods"](http://dl.acm.org/citation.cfm?doid=2872518.2889385) using the implementation provided in [this repository](https://github.com/gesiscss/image-gender-inference). More details can be found in the gender detection directory.

### Page Views

Todo...

## Scripts

### filter_edgelist_data.py 

As every file contains an edge lists for a specific month, i.e. 2016_5.csv - this is May 2016. Sometimes it is neded to filter out the files to a monthly **interval** 4m (every 4 months),6m (every 6 months),12m (every 12 months). Runing this script one should get all files in specified folder (**path_copy**), filter them according to the specified **interval**, and store them in the appropriate directory **path paste**

```{r, engine='bash', count_lines}
python filter_edgelist_data.py [path_copy] [path_paste] [interval]
```

### save_network.py 

The script iterates through the specified edge list files (**path_files**) , loads them as networkx graphs, and assignes attributes to all nodes of the graph. Finnaly, it saves each graph in a pickle in the specified location (**save_path**). It is also posible to choose the type of graph 'dir' for directed or 'undir' for undirected. Additionaly, a graph size (number of nodes and edges) statistic is generated in the end.

```{r, engine='bash', count_lines}
python save_network.py [path_files] [path_save] [graph_type]
```

### filter_graphs.py 

This script copies fiels from **path_copy** to **path_paste**. The files are specified in the **filter.csv** file.

```{r, engine='bash', count_lines}
python filter_graphs.py [path_copy] [path_paste] [filter.csv]
```

### calculate_efficiency.py (python 2.7.x)

This script loads **networkx** graphs, using the **gt2nx** implementation transforms them into **graph_tool** graphs, uses the **burt_measure.py** implementation to calculate efficiency. Outputs a csv file with node id and its efficiency.

```{r, engine='bash', count_lines}
python calculate_efficiency.py
```

### download.py 

This script sequentialy  downloads [Wikipedia pagecount dumps](https://dumps.wikimedia.org/other/pagecounts-raw/) [qzip]. **file.csv** contains a list of urls for the files mentioned. The **path_save** refers to directory where files should be downloaded. 

```{r, engine='bash', count_lines}
python download.py [file.csv] [path_save]
```

### downloader.py 

This script concurently downloads [Wikipedia pagecount dumps](https://dumps.wikimedia.org/other/pagecounts-raw/) [qzip]. **file.csv** contains a list of urls for the files mentioned. The **path_save** refers to directory where files should be downloaded. 

```{r, engine='bash', count_lines}
python downloader.py [file.csv] [path_save] [thread_number]
```
**THE SERVER CAN CURRENTLY NOT TAKE MORE THAN 3 THREADS

### parser.py
Opens specified list of files in **files_dir**, filters them per names in **names_file**, saves filtered files in **save_dir** using **num_threads** 
```{r, engine='bash', count_lines}
python parser.py [names_file] [files_dir] [save_dir] [num_threads]
```

### groupby.py

Loads files from **file_dir** as pandas dataframes, concatinates them, performs aggregation and saves them as csv on **save_path**. 

```{r, engine='bash', count_lines}
python groupby.py [file_dir] [save_path] 
```

## Notebooks

### hist_plot.py (python 2.7.x)

Saves 6 figures with two sub figures each. In this particular case, contains degree distribution, k_core distribution and efficiency distribution for both genders. 
```{r, engine='bash', count_lines}
python hist_plot.py
```

### add_stats_to_network.ipynb 

Inside of this notebook, properties and stats are added for each node of the graph

### add_efficiency.ipynb 

Inside of this notebook, efficiency, which was previously calculated using the graph_tool iplementation is transformed into a dictionary and then added to the networkx graphs.

### network_size.ipynb 

Plots - network size and ratio are produced with codes from this notebook


