from .models import VertexModel, EdgeModel


class Vertex:
    def __init__(self, node):
        self.id = str(node)
        self.adjacent = {}

    def add_adjacent(self, adjacent_vertex, weight=0):
        """Add to adjacency list the neighbors of this vertex
        args:
            adjacent_vertex: the neighbor node id
            weight: the 'distance' between two vertexes
        """
        self.adjacent[adjacent_vertex] = weight


class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight


class Graph:
    def __init__(self, graph_id):
        self.id = graph_id
        self.vertexes = dict()
        vertexes = VertexModel.objects.filter(graph_id=graph_id).values()  # probably exists a better way to do this
        edges = EdgeModel.objects.filter(graph_id=graph_id).values()

        for v in vertexes:
            self.add_vertex(Vertex(v['name']))

        for e in edges:
            edge = Edge(src=e['source_id'], dest=e['destination_id'], weight=e['weight'])
            self.connect(edge)

    def add_vertex(self, vertex: Vertex):
        """Add a new vertex to the graph"""
        self.vertexes[vertex.id] = vertex

    def connect(self, edge: Edge):
        """Connects two vertexes at the edge with its weight"""
        if edge.src not in self.vertexes:
            self.add_vertex(Vertex(edge.src))
        if edge.dest not in self.vertexes:
            self.add_vertex(Vertex(edge.dest))

        self.vertexes[edge.src].add_adjacent(edge.dest, edge.weight)
        self.vertexes[edge.dest].add_adjacent(edge.src, edge.weight)

    def get_vertex(self, vertex_id):
        v = self.vertexes.get(vertex_id)
        assert v, f"{vertex_id} not in {self.id}"
        return v

    def find_minimum_distance(self, src, dst=None):
        """Find minimum distance between two vertices based on its weight
        also known by Dijkstra algorithm
        args:
            src: key(id) - source vertex to start
            dst: key(id) - destination vertex
        return:
            dist: int distance between src and dst
            dist: dict previous connected vertexes
        """
        src = self.get_vertex(src)
        dst = self.get_vertex(dst)

        nodes = self.vertexes.keys()
        queue = set(nodes)

        dist = dict()
        prev = dict()

        for n in nodes:
            dist[n] = float('inf')
            prev[n] = None

        dist[src.id] = 0

        while queue:
            u = min(queue, key=dist.get)
            queue.remove(u)

            if dst.id is not None and u == dst.id:
                return dist[dst.id], prev

            for v, w in self.vertexes.get(u, ()).adjacent.items():
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        return dist, prev

    def find_path(self, previous, node):
        """Find (generate) path based on previous points
        args:
            previous: dict from previous connected vertexes given by find_minimum_distance
            node: key(name) of last point(vertex) of path
        return: the minimum path list like ['A', 'B', 'C']
        """
        node = self.vertexes.get(node)
        if node is None or previous == {}:
            return []

        path = []
        while node.id is not None:
            path.append(node.id)
            node.id = previous[node.id]
        return path[::-1]
