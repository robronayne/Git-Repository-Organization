import os, sys, zlib
node_dict = {}
    
class CommitNode:
    def __init__(self):
        self.parents = list()
        self.children = list()
        self.branch_name = list()
        self.indegree = 0
        
# Find out if the folder is within a repository
def repo_path(cwd):
    git_repo = False # Initially unsure if we are in a repo

    while True:
        files_in_cwd = os.listdir(cwd)
        # Search the cwd for the .git directory                                                                                    
        for file in files_in_cwd:
            if file == '.git':
                git_repo = True
                path = cwd + '/' + file
        # If git repo found, or the '/' dir is reached, stop searching
        if git_repo == True or cwd =='/':
            break
        
        # Set the cwd to the parent directory                                                                                 
        cwd = os.path.dirname(cwd)

    if not git_repo:
        sys.stderr.write("Not inside a Git repository")
        exit(1)

    return path

# Get dir name from hash        
def get_node_dir(node):
    return node[:2]

# Get object name from hash
def get_node_file(node):
    return node[2:]

# Open the object file and read from it
def find_node(node, node_path):
    os.chdir(node_path)
    commit = open(node)
    node = commit.read().strip()
    commit.close()
    return node

# Decompress the object for information
def get_node_data(node, object_dir):
    os.chdir(object_dir + get_node_dir(node))
    commit = open(get_node_file(node), 'rb')
    node_bytes = zlib.decompress(commit.read()) 
    node_data = str(node_bytes, 'UTF-8')
    commit.close()
    return node_data
    
# Read the parent hashes of the commit
def list_parents(node_data):
    parents = []
    parent_hash_loc = 0
    substr = "\nparent "
    hash_length = 40 + len(substr)

    # Search for the substring containing '\nparent'
    # and locate the following hash
    while True:
        parent_hash_loc = node_data.find(substr, parent_hash_loc)
        if parent_hash_loc == -1:
            return parents
        parents.append(node_data[parent_hash_loc+len(substr):parent_hash_loc+hash_length])
        parent_hash_loc += len(substr)

# Depth-first-search algorithm
def dfs(visited, node, object_dir):
    if node not in visited:
        # Node has now been visited, add it to the dict if it has not already
        visited.append(node)
        if node not in node_dict:
            node_dict[node] = CommitNode()

        node_parents = list_parents(get_node_data(node, object_dir))
            
        # Update the node's parents
        node_dict[node].parents = node_parents
        
        # Recursively add the parents
        for parent in node_parents:
            dfs(visited, parent, object_dir)

# For each node, find a parent-child relationship
def find_children():
    for child in node_dict.keys():
        for parent in node_dict[child].parents:
            node_dict[parent].children.append(child)
        
def kahns_alg():
    L = list() # Will contain sorted elements
    S = list() # Will contain nodes with no incoming edge

    # Update the indegree for all nodes
    for node in node_dict:
        node_dict[node].indegree = len(node_dict[node].children)
        
    # Initialize S to starting elements with 0 indegree
    for node in node_dict:
        if node_dict[node].indegree == 0:
            S.append(node)

    # Sort the starting list so we generate the same output each time
    S.sort()
    
    while S:
        n = S.pop(0) # Remove first node from S
        L.append(n) # Append node to L
        
        # For each node with edge from n to m, remove edge
        for m in node_dict[n].parents:
            node_dict[m].indegree = node_dict[m].indegree - 1
            # If m has no other incoming edges
            if node_dict[m].indegree == 0:
                S.insert(0,m)
       
    # Check the graph for cycles
    for node in L:
        if node_dict[node].indegree != 0:
            sys.stderr.write("Sorting failed, graph has a cycle")
            exit(2)
            
    return L

# Print parents of the last node with an '=' at the end
def print_sticky_end(node):
    size = len(node.parents)
    for index in range(0,size):
        if index < size-1:
            print(node.parents[index])
        else:
            print(node.parents[index], end='=\n\n')
            
# Print an '=' before listing the children of the current node
def print_sticky_start(node):
    if node.children:
        size = len([node.children])

        print('=', end='')
        for index in range(0,size):
            if index < size-1:
                print(node.children[index], end=' ')
            else:
                print(node.children[index])
    else:
         print('=')

# Print ref tags
def print_tags(node):
    node.branch_name.sort
    size = len(node.branch_name)
    for index in range(0,size):
        if index < size-1:
            print(node.branch_name[index], end=' ')
        else:
            print(node.branch_name[index])

# Output the topologically sorted commits
def topo_print():
    topo = kahns_alg()
    size = len(topo)
    sticky_printed = False
    
    # Loop through the commits and determine if sticky outputs need to be generated
    for index in range(0,size):
        # Print a sticky start for lines separated by whitespace
        if sticky_printed:
            print_sticky_start(node_dict[topo[index]])
            sticky_printed = False
            
        # If a branch names are attached to the current commit print it with output
        if node_dict[topo[index]].branch_name:
            print(topo[index], end=' ')
            print_tags(node_dict[topo[index]])
        else:
            print(topo[index])
        
        # If not at the end of the list and next commit is not parent of current commit
        if index < size-1 and topo[index+1] not in node_dict[topo[index]].parents:
            print_sticky_end(node_dict[topo[index]])
            sticky_printed = True

def topo_order_commits():
    path = repo_path(os.getcwd()) 
    heads_dir = path + '/refs/heads/'
    object_dir = path + '/objects/'
    
    heads_in_dir = os.listdir(heads_dir)
    # Search the heads in the /refs/heads dir
    for head in heads_in_dir:
        node = find_node(head, heads_dir)

        # Update node information in the dictionary
        if node not in node_dict:
            node_dict[node] = CommitNode()
            node_dict[node].parents = list_parents(get_node_data(node, object_dir))
            node_dict[node].branch_name.append(head)

            # Perform a DFS on each head
            dfs(list(),node,object_dir)

        # Add the additional branch name to the tag
        else:
            node_dict[node].branch_name.append(head) 

    find_children()
    topo_print()

if __name__ == '__main__':
    topo_order_commits()
