# Wikipedia-Politician-Network

## Dataset

The dataset with additional information about it is available on the following adress: https://datorium.gesis.org/xmlui/handle/10.7802/1515

The data used for this project is located in the politician-data-wikipedia-edge-list.zip file, which contains: 
* Edge list files - containing edges between politician pages on Wikipedia through time
* Politician data - data about the politicians that can be found on Wikipedia

### filter_edgelist_data.py 

As every file contains an edge lists for a specific month, i.e. 2016_5.csv - this is May 2016. Sometimes it is neded to filter out the files to a monthly **interval** 4m (every 4 months),6m (every 6 months),12m (every 12 months). Runing this script one should get all files in specified folder (**path_copy**), filter them according to the specified **interval**, and store them in the appropriate directory **path paste**

```{r, engine='bash', count_lines}
python filter_edgelist_data.py [path_copy] [path_paste] [interval]
```

### save_network.py 

The script iterates through the specified edge list files (**path_files**) , loads them as networkx graphs, and assignes attributes to all nodes of the graph. Finnaly, it saves each graph in a pickle in the specified location (**save_path**). It is also posible to choose the type of graph 'dir' for directed or 'undir' for undirected. Additionaly, a graph size statistic is generated in the end.

```{r, engine='bash', count_lines}
python save_network.py [path_files] [path_save] [graph_type]
```
