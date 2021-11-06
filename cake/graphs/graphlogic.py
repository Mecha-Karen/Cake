from __future__ import annotations


class Graph(object):
    """
    Graphs are represented as a dictionary structure, but are instantiated
    through **kwargs here is an example:

    The assignment:
    graph = Graph(node1=["node2"], node2=["node3"], node3=["node1", "node2", "node4"], node4=["node1", "node3"])

    Corresponds to:
    graph = [
      "node1" : [ "node2" ], "node2" : [ "node3" ],
      "node3" : [ "node2", "node1", "node4" ], "node4" : ["node1", "node3"],
    ]

    .. code-block:: py

        >>> from cake import Graph
        >>> graph = Graph(node1=["node2"], node2=["node3"], node3=["node1", "node2", "node4"], node4=["node1", "node3"])
        >>> graph.list_all_vertices()
        ['node3', 'node1', 'node4', 'node2']

        >>> graph.list_edges("node3")
        ['node1', 'node4', 'node2']

        >>> graph.add_vertex("node5")
        >>> graphObject.list_all_vertices()
        ['node2', 'node1', 'node5', 'node3', 'node4']

        >>> graph.add_edge(["node2","node4"])
        >>> graph.list_edges("node2")
        ['node4', 'node3']

    """

    def __init__(self, graph: dict = None, **nodes):
        # instantiates a graph object, if no dict is supplied, use an empty one
        if not nodes:
            nodes = dict()

        if graph:
            # Allow use of basic dictionary insertions
            nodes = {**graph, **nodes}

        if any(i for i in nodes.values() if not isinstance(i, list)):
            raise ValueError("Cannot bind graph, invalid structure provided")

        self._nodes = nodes
        self._weights = dict()

    def listNodeEdges(self, node: str) -> list:
        """returns a list of the node heads"""
        return self._nodes[node]

    def listEdges(self) -> set:
        """returns all the different edges in a graph"""
        cms = [self._nodes[i] for i in self._nodes]
        x = map(lambda x: " ".join(x), cms)
        return " ".join(x).split(" ")

    def listNodes(self) -> set:
        """returns all the nodes in the graph"""
        return set(self._nodes.keys())

    def addNode(self, node: str, *edges) -> None:
        """adds a vertex to the graph by inserting positionally into the graph dict"""

        if node not in self.graph_structure_dict:
            self.graph_structure_dict[node] = list(edges)

    def addEdge(self, node: str, edge: str) -> None:
        """Add a edge to a node, if edge is not already in node"""
        if edge in self._nodes[node]:
            # Dont add to node
            raise ValueError(f"Cannot add `{edge}` to `{node}`, as edge already exists")

        self._nodes[node].append(edge)

    @property
    def nodeCount(self):
        return len(self._nodes)

    def __lt__(self, O: Graph) -> bool:
        """N.nodeCount < O.nodeCount"""
        return self.nodeCount < O.nodeCount

    def __le__(self, O: Graph) -> bool:
        """N.nodeCount <= O.nodeCount"""
        return self.nodeCount < O.nodeCount

    def __gt__(self, O: Graph) -> bool:
        """N.nodeCount > O.nodeCount"""
        return self.nodeCount > O.nodeCount

    def __ge__(self, O: Graph) -> bool:
        """N.nodeCount >= O.nodeCount """
        return self.nodeCount >= O.nodeCount
