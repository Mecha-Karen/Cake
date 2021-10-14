class Graph(object):

    """
    Graphs are represented as a dictionary structure, here is an example:

    graph = { 
      "node1" : { "node2" }, "node2" : { "node3" },
      "node3" : { "node2", "node1", "node4" }, "node4" : {"node1", "node3"},
    }

    Example
    ^^^^^^^
    .. code-block:: py

        >>> from cake import Graph
        >>> graph = {
        ...       "node1" : { "node2" }, "node2" : { "node3" },
        ...       "node3" : { "node2", "node1", "node4" }, "node4" : {"node1", "node3"},
        ...     }

        >>> graphObject = Graph(graph)
        >>> graphObject.list_all_vertices()
        {'node3', 'node4', 'node1', 'node2'}

        >>> graphObject.list_edges("node4")
        {'node3', 'node1'}

        >>> graphObject.add_vertex("node5")
        >>> graphObject.list_all_vertices()
        {'node4', 'node5', 'node2', 'node3', 'node1'}
    """

    def __init__(self, graph_structure_dict=None):
        # instantiates a graph object, if no dict is supplied, use an empty one
        if graph_structure_dict == None:
            graph_structure_dict = {}
        self.graph_structure_dict = graph_structure_dict

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

