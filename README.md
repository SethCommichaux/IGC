# Code used for the critical analysis of the IGC
The Integrated Gene Catalog (IGC) is a set of nearly 10 million reference genes from the human gut microbiome.

## Identifying all the cluster members of IGC representatives
The IGC provides the representative sequences from gene clustering as a reference database. For our analysis, however, we needed all the cluster members that clustered to their representative sequences. These relationships can be determined from the CD-Hit clustering output files that the IGC author's [provided](http://gigadb.org/dataset/100064) (i.e. AGC.clstr, EGC.clst, CGC.clstr, SPGC.clstr, 3CGC.clstr and IGC.clstr) using the script trace_cluster_generations.py run from a directory where all of the \*clstr files are.

```
python trace_cluster_generations.py
```

This script creates two files: 1) edge_list.txt, which provides all representative-redundant sequence clustering relationships in the IGC; 2) adjacency_list.txt, which provides an adjacency list for cluster membership in the IGC.

## Transitive clustering error analysis

Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

foobar.pluralize('word') # returns 'words'
foobar.pluralize('goose') # returns 'geese'
foobar.singularize('phenomena') # returns 'phenomenon'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
