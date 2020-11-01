from django.db import models


class VertexModel(models.Model):
    name = models.CharField(max_length=10)
    graph_id = models.CharField(max_length=20)


class EdgeModel(models.Model):
    source_id = models.CharField(max_length=10)
    destination_id = models.CharField(max_length=10)
    weight = models.IntegerField()
    graph_id = models.CharField(max_length=20)


