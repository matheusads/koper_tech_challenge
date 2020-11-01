from .models import VertexModel, EdgeModel
from .serializers import VertexSerializer, EdgeSerializer, RouterQueryValidator
from .graph_handlers import Graph
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError


class VertexView(ModelViewSet):
    queryset = VertexModel.objects.all()
    serializer_class = VertexSerializer


class EdgeView(ModelViewSet):
    queryset = EdgeModel.objects.all()
    serializer_class = EdgeSerializer


class BestRoute(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        try:
            data = RouterQueryValidator().run_validation(request.query_params)
            graph_id = data.get('map')
            source = data.get('source')
            dest = data.get('dest')
            range_avg = data.get('range')
            price = data.get('price')
        except ValidationError as err:
            raise ValidationError(err.detail)

        graph = Graph(graph_id)
        try:
            distance, previous = graph.find_minimum_distance(source, dest)
        except AssertionError as err:
            return Response(err.args[0])

        path = graph.find_path(previous, dest)
        cost_per_km = price / range_avg
        final_cost = cost_per_km * distance

        return Response(f"{source} -> {dest}: distance = {distance}, path = {path}, cost = {final_cost}")
