class Node(object):
    def __init__(self, name):
        """
            Assumes name is a string
        """
        self.name = name
    def getName(self):
        return self.name
    def __str__(self):
        return self.name


class Edge(object):
    def __init__(self, src, dest):
        """
            Assumes src and dest are nodes
        """
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()


class Digraph(object):
    """
        edges is a dict mapping each node to a list of its children
    """
    def __init__(self):
        self.edges = {}

    def addNode(self, node):
        if node in self.edges:
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []
    
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()

        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)

    def childrenOf(self, node):
        return self.edges[node]

    def hasNode(self, node):
        return node in self.edges

    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)

    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->' + dest.getName() + '\n'

        # omit the final newline
        return result[:-1]


class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


nodes = []
nodes.append(Node("ABC")) # nodes[0]
nodes.append(Node("ACB")) # nodes[1]
nodes.append(Node("BAC")) # nodes[2]
nodes.append(Node("BCA")) # nodes[3]
nodes.append(Node("CAB")) # nodes[4]
nodes.append(Node("CBA")) # nodes[5]


g = Graph()
for n in nodes:
    g.addNode(n)

# Iterate through the list of nodes, excluding the final node
for i in nodes[:-1]:
    # Compare to all the nodes in front
    for j in nodes[nodes.index(i)+1:]:
        # Swap flagged True if an edge can be established between two nodes
        swap = False
        # For every char (student) in the string (line) . . .
        for node in range(len(i.getName()[:-1])):
            # If an adjacent swap has occured . . .
            if i.getName()[node] == j.getName()[node + 1] and \
                i.getName()[node + 1] == j.getName()[node]:

                # Flagged True for a swap bewteen two adjacent chars (students)
                swap = True
        # Add the edge to the Graph instance, g
        if swap:
            g.addEdge(Edge(i, j))


edges = g.childrenOf(nodes[1])
for ed in edges:
    print(ed)