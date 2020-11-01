from django.test import TestCase
from rest_framework.test import APIClient
from .graph_handlers import Vertex, Edge, Graph
from .models import VertexModel, EdgeModel


class GraphTest(TestCase):
    def setUp(self) -> None:
        VertexModel(name='A', graph_id='Map').save()
        VertexModel(name='B', graph_id='Map').save()
        VertexModel(name='C', graph_id='Map').save()
        VertexModel(name='D', graph_id='Map').save()
        VertexModel(name='E', graph_id='Map').save()
        VertexModel(name='F', graph_id='Not').save()

        EdgeModel(source_id='A', destination_id='B', weight=10, graph_id='Map').save()
        EdgeModel(source_id='B', destination_id='D', weight=15, graph_id='Map').save()
        EdgeModel(source_id='A', destination_id='C', weight=20, graph_id='Map').save()
        EdgeModel(source_id='C', destination_id='D', weight=30, graph_id='Map').save()
        EdgeModel(source_id='B', destination_id='E', weight=50, graph_id='Map').save()
        EdgeModel(source_id='D', destination_id='E', weight=50, graph_id='Map').save()
        EdgeModel(source_id='F', destination_id='G', weight=50, graph_id='Not').save()

        self.graph = Graph(graph_id='Map')
        self.client = APIClient()

    def test_find_min_distance(self):
        """Test find distance and path between two adjacent points"""
        distance, previous = self.graph.find_minimum_distance('B', 'D')
        path = self.graph.find_path(previous, 'D')
        self.assertEqual(distance, 15)
        self.assertEqual(path, ['B', 'D'])

    def test_find_min_dist_long(self):
        """Test find distance and path between two points not adjacent"""
        dist, prev = self.graph.find_minimum_distance('A', 'E')
        path = self.graph.find_path(prev, 'E')
        self.assertEqual(dist, 60)
        self.assertEqual(path, ['A', 'B', 'E'])

    def test_find_min_distance_should_fail(self):
        """Test with points not in Map graph"""
        self.assertRaises(AssertionError, self.graph.find_minimum_distance, 'A', 'G')  # 'A' in map, G not
        self.assertRaisesMessage(AssertionError, "G not in Map")
        self.assertRaises(AssertionError, self.graph.find_minimum_distance, 'F', 'G')  # Both not in map
        self.assertRaisesMessage(AssertionError, "F not in Map")

    def test_find_path(self):
        """Test to generate path same as A to E points """
        previous = {'A': None, 'B': 'A', 'C': 'A', 'D': 'B', 'E': 'B'}
        path = self.graph.find_path(previous, 'E')
        self.assertEqual(path, ['A', 'B', 'E'])

    def test_find_broken_path(self):
        """Test with empty path"""
        path = self.graph.find_path({}, 'A')
        self.assertEqual(path, [])

    def test_find_path_no_node(self):
        """Test with node not in graph"""
        previous = {'A': None, 'B': 'A', 'C': 'A', 'D': 'B', 'E': 'B'}
        path = self.graph.find_path(previous, 'G')  # G not in map
        self.assertEqual(path, [])
        path = self.graph.find_path({}, 'G')  # G and previous not in map
        self.assertEqual(path, [])

    #  Here tests for basic methods like connect and adds

    def test_add_adjacency(self):
        """Test add a neighbor in vertex class representation"""
        v = Vertex('X')
        self.assertEqual(v.adjacent, {})
        v.add_adjacent('Y')  # no weight
        self.assertEqual(v.adjacent, {'Y': 0})
        v.add_adjacent('Z', 100)
        self.assertEqual(v.adjacent, {'Y': 0, 'Z': 100})

    def test_add_vertex_in_graph(self):
        """Test to add a new point in graph"""
        v = Vertex('N')
        self.assertRaises(AssertionError, self.graph.get_vertex, 'N')  # check not in graph
        self.graph.add_vertex(v)
        self.assertEqual(v, self.graph.get_vertex('N'))

    def test_connect_edges(self):
        """Test connect points in the edge to the graph"""
        e = Edge('G', 'F', 10)
        self.assertRaises(AssertionError, self.graph.get_vertex, 'G')  # check not in
        self.assertRaises(AssertionError, self.graph.get_vertex, 'F')
        self.graph.connect(e)
        g = self.graph.get_vertex('G')
        f = self.graph.get_vertex('F')
        self.assertIsNotNone(g)
        self.assertIsNotNone(f)
        self.assertEqual(g.adjacent, {'F': 10})
        self.assertEqual(f.adjacent, {'G': 10})

    # From Here some api(views) tests, in a bigger project is recommended put in other file
    # I put here to not duplicated code creating vertexes and edges

    def test_get_from_api_map_not_in_db(self):
        """Test get from A to E points but with different Map name(graph id)"""
        r = self.client.get('/routes/', {'map': 'Mapa SP', 'source': 'A', 'dest': 'E', 'range': 10, 'price': 2.5})
        self.assertEqual(r.data, 'A not in Mapa SP')
        self.assertEqual(r.status_code, 200)

    def test_get_from_api_success(self):
        """Test get from A to D points"""
        r = self.client.get('/routes/', {'map': 'Map', 'source': 'A', 'dest': 'D', 'range': 10, 'price': 2.5})
        self.assertEqual(r.data, "A -> D: distance = 25, path = ['A', 'B', 'D'], cost = 6.25")
        self.assertEqual(r.status_code, 200)

    def test_api_validation_error(self):
        """Test with some params missing"""
        expected_msg = b'{"range":["This field is required."],"price":["This field is required."]}'
        r = self.client.get('/routes/', {'map': 'Map', 'source': 'A', 'dest': 'D'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.content, expected_msg)
