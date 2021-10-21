class Graph(object):

    """
    Graphs are represented as a dictionary structure, but are instantiated
    through **kwargs here is an example:
    
    The assignment:
    graph = Graph(node1={"node2"}, node2={"node3"}, node3={"node1", "node2", "node4"}, node4={"node1", "node3"})
    
    Corresponds to:
    graph = { 
      "node1" : { "node2" }, "node2" : { "node3" },
      "node3" : { "node2", "node1", "node4" }, "node4" : {"node1", "node3"},
    }

    Example
    ^^^^^^^
    .. code-block:: py

        >>> from cake import Graph
        >>> graph = Graph(node1={"node2"}, node2={"node3"}, node3={"node1", "node2", "node4"}, node4={"node1", "node3"})
        >>> graph.list_all_vertices()
        {'node3', 'node1', 'node4', 'node2'}

        >>> graph.list_edges("node3")
        {'node1', 'node4', 'node2'}

        >>> graph.add_vertex("node5")
        >>> graphObject.list_all_vertices()
        {'node2', 'node1', 'node5', 'node3', 'node4'}

        >>> graph.add_edge({"node2","node4"})
        >>> graph.list_edges("node2")
        {'node4', 'node3'}

    """

    def __init__(self, **graph_structure):
        # instantiates a graph object, if no dict is supplied, use an empty one
        if graph_structure == None:
            graph_structure = {}
        self.graph_structure_dict = graph_structure

    def list_edges(self, vertice):
        # returns a list containing the vertice's edges
        return self.graph_structure_dict[vertice]
        
    def list_all_vertices(self):
        # returns all a graph's vertices 
        return set(self.graph_structure_dict.keys())

    def add_vertex(self, vertex):
        # adds a vertex to the graph by inserting positionally into the graph dict
        if vertex not in self.graph_structure_dict:
            self.graph_structure_dict[vertex] = []
    
    def add_edge(self, edge):
        edge = set(edge)
        start_vertex, end_vertex = tuple(edge)
        for start, end in [(start_vertex, end_vertex), (end_vertex, start_vertex)]:
            if start in self.graph_structure_dict:
                self.graph_structure_dict[start].add(end)
            else:
                self.graph_structure_dict[start] = [end]
