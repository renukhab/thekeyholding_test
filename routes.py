from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from models import db, Gate, Route
import heapq
import json
from flask import Blueprint

# Create Flask Blueprint
api_blueprint = Blueprint("api", __name__, url_prefix="/api")

# Attach API to Blueprint
api = Api(api_blueprint, version="1.0", title="Interstellar Route Planner API",
          description="API for calculating travel costs and finding the shortest routes between space gates.")
ns = api.namespace("", description="Routes")

### Swagger Models ###
gate_model = api.model("Gate", {
    "id": fields.String(description="Gate ID (3-letter code)", required=True, example="SOL"),
    "name": fields.String(description="Gate name", required=True, example="Sol"),
    "connections": fields.Raw(description="Connections to other gates with distances", example=[{"id": "PRX", "hu": 90}])
})

route_model = api.model("Route", {
    "source_gate_id": fields.String(description="Source gate ID", required=True, example="SOL"),
    "destination_gate_id": fields.String(description="Destination gate ID", required=True, example="PRX"),
    "hyperplane_units": fields.Float(description="Distance in Hyperplane Units (HU)", required=True, example=90.0)
})

transport_response_model = api.model("TransportCost", {
    "cheapest": fields.String(description="Cheapest transport type", example="HSTC Transport"),
    "cost": fields.Float(description="Total cost of the transport", example=45.0)
})

route_response_model = api.model("ShortestRoute", {
    "route": fields.List(fields.String, description="Shortest path from source to destination"),
    "cost": fields.Float(description="Total cost of the journey")
})

### GET ALL GATES ###
@ns.route("/gates")
class GateList(Resource):
    @api.marshal_list_with(gate_model)
    def get(self):
        """Retrieve all gates"""
        gates = Gate.query.all()
        return gates

### GET A SINGLE GATE ###
@ns.route("/gates/<string:gate_code>")
@api.doc(params={"gate_code": "3-letter gate code"})
class GateDetail(Resource):
    @api.marshal_with(gate_model)
    def get(self, gate_code):
        """Retrieve details of a specific gate"""
        gate = Gate.query.filter_by(id=gate_code).first()
        if not gate:
            api.abort(404, "Gate not found")
        return gate

### TRANSPORT COST CALCULATION ###
@ns.route("/transport/<float:distance>")
@api.doc(params={"distance": "Distance to the nearest gate (in AU)", "passengers": "Number of passengers", "parking": "Days of parking"})
class TransportCost(Resource):
    @api.marshal_with(transport_response_model)
    def get(self, distance):
        """Calculate the cheapest transport cost based on distance"""
        passengers = int(request.args.get("passengers", 1))
        parking_days = int(request.args.get("parking", 0))

        personal_cost = (0.30 * distance) + (5 * parking_days)
        hstc_cost = 0.45 * distance

        cheapest = "HSTC Transport" if hstc_cost < personal_cost else "Personal Transport"

        return {"cheapest": cheapest, "cost": min(personal_cost, hstc_cost)}

@ns.route("/nearest-gate/<float:distance>")
@api.doc(params={"distance": "Distance from current location to nearest gate in AU"})
class NearestGate(Resource):
    def get(self, distance):
        """Find the nearest gate based on connections"""
        nearest_gate = None

        for gate in Gate.query.all():
            if gate.connections:  # Ensure connections exist
                for item in gate.connections:
                    if float(item["hu"]) <= distance:
                        nearest_gate = gate
                        break

        if not nearest_gate:
            api.abort(404, "No gates found within the given distance")

        return {"nearest_gate": nearest_gate.id, "name": nearest_gate.name}


### SHORTEST ROUTE BETWEEN TWO GATES ###
@ns.route("/gates/<string:source_gate>/to/<string:destination_gate>")
@api.doc(params={"source_gate": "Source gate code", "destination_gate": "Destination gate code"})
class ShortestRoute(Resource):
    @api.marshal_with(route_response_model)
    def get(self, source_gate, destination_gate):
        """Find the cheapest route between two gates considering one-way distances"""
        gates = {g.id: g for g in Gate.query.all()}

        if source_gate not in gates or destination_gate not in gates:
            api.abort(404, "Invalid gate codes")

        graph = {gate.id: {} for gate in gates.values()}
        for route in Route.query.all():
            graph[route.source_gate_id][route.destination_gate_id] = route.hyperplane_units

        path, cost = dijkstra(graph, source_gate, destination_gate)

        if not path:
            api.abort(404, "No route found")

        return {"route": path, "cost": cost}

### DIJKSTRA'S ALGORITHM FOR ONE-WAY ROUTES ###
def dijkstra(graph, start, target):
    pq = [(0, start, [])]
    visited = set()

    while pq:
        (cost, gate, path) = heapq.heappop(pq)
        if gate in visited:
            continue
        path = path + [gate]
        visited.add(gate)

        if gate == target:
            return path, cost

        for neighbor, travel_cost in graph[gate].items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + travel_cost, neighbor, path))

    return None, float('inf')
