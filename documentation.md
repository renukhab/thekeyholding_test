# **Interstellar Route Planner API Documentation**

## **Overview**
The Interstellar Route Planner API provides endpoints to:
- Retrieve gate information.
- Calculate the cheapest transport option from a location to the nearest gate.
- Determine the shortest route between two gates using a hyperspace network.
- Find the nearest gate based on distance in Astronomical Units (AU).

## **API Endpoints**

### **1. Retrieve All Gates**
**Endpoint:** `GET /api/gates`

**Description:** Returns a list of all available hyperspace gates.

**Response:**
```json
[
    {
        "id": "SOL",
        "name": "Sol",
        "connections": [
            { "id": "PRX", "hu": 90 }
        ]
    },
    {
        "id": "PRX",
        "name": "Proxima",
        "connections": [
            { "id": "SOL", "hu": 90 }
        ]
    }
]
```

---

### **2. Retrieve a Single Gate**
**Endpoint:** `GET /api/gates/{gateCode}`

**Description:** Fetches details of a specific gate by its gate code.

**Request Parameters:**
- `gateCode` (string): 3-letter code representing the gate.

**Response:**
```json
{
    "id": "SOL",
    "name": "Sol",
    "connections": [
        { "id": "PRX", "hu": 90 }
    ]
}
```

---

### **3. Calculate Transport Cost**
**Endpoint:** `GET /api/transport/{distance}?passengers={number}&parking={days}`

**Description:** Determines the cheapest transport method for traveling to the nearest gate.

**Request Parameters:**
- `distance` (float, required): Distance to the gate in Astronomical Units (AU).
- `passengers` (int, optional, default=1): Number of passengers.
- `parking` (int, optional, default=0): Number of days of vehicle storage at the gate.

**Response:**
```json
{
    "cheapest": "HSTC Transport",
    "cost": 45.0
}
```

---

### **4. Find the Nearest Gate**
**Endpoint:** `GET /api/nearest-gate/{distance}`

**Description:** Identifies the closest gate based on a given real-space distance in AU.

**Request Parameters:**
- `distance` (float, required): Distance from the current location in AU.

**Response:**
```json
{
    "nearest_gate": "SOL",
    "distance": 1.0
}
```

---

### **5. Find the Shortest Route Between Two Gates**
**Endpoint:** `GET /api/gates/{sourceGate}/to/{targetGate}`

**Description:** Determines the optimal route between two gates using the hyperspace network.

**Request Parameters:**
- `sourceGate` (string, required): The starting gate code.
- `targetGate` (string, required): The destination gate code.

**Response:**
```json
{
    "route": ["SOL", "PRX", "ALT"],
    "cost": 240.0
}
```

---

## **Algorithm Used**

### **Dijkstra’s Algorithm for Shortest Path**

**Why Dijkstra's Algorithm?**
- Efficiently finds the shortest path in a weighted graph.
- Suitable for routing problems where edge weights (distances) vary.
- Guarantees the optimal path for one-way hyperspace routes with asymmetric distances.

**Implementation Steps:**
1. **Initialize:**
   - Set the starting gate’s cost to `0` and all other gates to infinity (`∞`).
   - Use a priority queue to track the next gate to explore.
2. **Process Gates:**
   - Extract the gate with the lowest cost.
   - Update the travel cost for its connected gates.
3. **Update Paths:**
   - If a shorter path is found to a connected gate, update the cost.
   - Continue processing until reaching the target gate or exhausting possible paths.
4. **Return Result:**
   - If the target gate is reached, return the route and cost.
   - If no valid route exists, return an error message.

**Code Example:**
```python
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
```

---

## **Conclusion**
This API provides a robust and efficient system for interstellar route planning. By utilizing:
- **Flask** for API development.
- **PostgreSQL** for data persistence.
- **Dijkstra’s algorithm** for optimal route calculations.
- **Flask-RESTx** for API documentation and structure.

This ensures a scalable, efficient, and well-documented solution for hyperspace navigation.

For further improvements, we can implement caching mechanisms, optimize the database queries, and enhance logging for better traceability.

