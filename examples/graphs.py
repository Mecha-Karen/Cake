from cake import Graph
# We can represent graphs by describing the nodes and their relationships as a dict
graph = Graph(node1={"node2"}, node2={"node3"}, node3={"node1", "node2", "node4"}, node4={"node1", "node3"})

# We can list the vertices that the graph contains like so:
graph.list_all_vertices()
# Result = {'node3', 'node1', 'node4', 'node2'}

# Equally,. we can list the edges we described in our original structure
graph.list_edges("node3")
# Result = {'node1', 'node4', 'node2'}

# We can modify the graph, for example by adding vertexes
graph.add_vertex("node5")
graphObject.list_all_vertices()
# Result # {'node2', 'node1', 'node5', 'node3', 'node4'}

# Or by adding edges to connect vertexes
graph.add_edge({"node2","node4"})
graph.list_edges("node2")
# Result = {'node4', 'node3'}
