# Topological Sort of Git Commits

This assignment was the sixth and final assignment completed while taking Software Construction with [Professor Eggert](https://samueli.ucla.edu/people/paul-eggert/). This quarter's course webpage can be accessed [here](https://web.cs.ucla.edu/classes/fall21/cs35L/index.html). 

## About

This Python script produces a graph of Git commits in topological order. In addition to displaying commit hashes, the branch names will also be listed next to the corresponding hash. The motivation behind this is to generate the graph *without* using any Git commands. Only the modules in the Python Standard Library may be used: **os**, **sys** and **zlib**.
 
Complete information regarding the project specifications can be seen in the Git Repository Organization pdf file that is included.

## Usage

For proper use, simply navigate to a directory that already contains a Git repository and run `python3 topo_order_commits.py` to invoke the script. Output will be displayed in the terminal window. 

Running the script within a directory that does not contain a Git repository  will result in an error message.