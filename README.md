**Basic API Project to Python dev role at [Koper](https://koper.com.br/)**

You can find the project scope at [Desafio back-end PDF File](Desafio back-end.pdf) in PT-Br

Tldr: API should return minimum route between two points, previously inserted, and how much it costs.


**Project Stack**

I choose use minimum possible external libs, so in this project I only used Django with Django Rest Framework 
because they allow me a fast development and didn't need to worry with database configuration for example. 
So for this I didn't use pytest(my preference) or a lib to resolve the Graph problem.

For development and tests I used PyCharm, Postman and [DRF Browsable API](https://restframework.herokuapp.com/) 
in Elementary OS (Ubuntu based)


**Project Setup**

Python 3.6 - was the default in my system
Virtualenv

Clone project
```
git clone git@github.com:matheusads/koper_tech_challenge.git
```

Make a virtualenv with at least Python 3.6
```
python3 -m venv
```

Activate virtualenv
```
source venv/bin/activate
```

Install dependencies
```
pip install -r requirements.txt
```
Make migrations
```
python manage.py makemigrations
python manage.py migrate
```
Create a superuser.
```
python manage.py creatersuperuser
```
Then finally run server
```
python manage.py runserver
```

Unit tests
```
python manage.py test
```

**API usage**

As this is a small POC, to insert data we can use Browsable API, Django Admin or APIs 
requests as in Postman Collection (recommended). For lot of data I would make a [management script](https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/)  

We need to add some _points(vertexes)_ to a _map(graph)_ and _connect(edges_) the points.

At ``/vertex`` POST should send through body request some data like this `{'name': 'A', 
                                                                            graph_id: 'Map Name'}`
**_Name_**: A string field with 10 characters max length. This will be a place in map. 
_**Graph_ID**_: A string field with 20 characters max length. This will be the 'map name'

At ``/edge`` POST should send some like this `{'source_id': 'A', 'destination_id': 'B', 
                                                'weight': 10, 'graph_id': 'Map Name'}`    

**_Source_id_** and Destination_id: The names of two connected points. Char Field 10 max length.
**_Graph_ID_**: Same as `/vertex`
**_Weight_**: Integer field, is the 'distance' between these two points.

I didn't add unit tests for these endpoints because is a 'simply' code of DRF. Just put to have Browsable APIs
and fast way to add data. But have some test in [Postman](Koper Test Collection.postman_collection.json) json file.

**_The most important part_**

At ``/routes`` we only have GET method and need send the follow query params
`{'map': 'Mapa SP', 'source': 'A', 'dest': 'D', 'range': 10, 'price': 2.5 }`

**_Map_**, **_source_** and **_dest_** is the previously graph_id, source_id(vertex name) and destination_id(second vertex name).
**_Range_** is the range average car capacity per liters. Decimal field, so can pass almost any type of number.   
**_Price_** is the fuel's value per liter. Also Decimal field.
All these fields are **required** and **validate**.

This endpoint has three possible responses.
- ValidationError, raised if some field of query not in the right format or missing.
- AssertionError, a formated Response if some _Point(source ou dest)_ not in given _Map_.
- The expected Response with given points, the distance and path between them, e the cost to go through.
 
A possible response is:
``"A -> D: distance = 25, path = ['A', 'B', 'D'], cost = 6.25"``

**_PS:_**

To resolve the minimum distance problem I use [Dijkstra Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm).

I choose code readability so the Graph, Vertex and Edge representations could be more simple and fast,
but thinking in who will read I opt for this way.

For the sake of simplicity of these project I also didn't use git branches.
My commit are have a lot of code too. In real case it should be with small pieces of code.

