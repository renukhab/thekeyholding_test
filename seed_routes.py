from app import app, db
from models import Gate, Route

with app.app_context():
    # Fetch all gates and create a dictionary mapping gate ID to gate object
    gates = {gate.id: gate for gate in Gate.query.all()}

    # Define routes based on the provided graph
    routes_data = [
        ("SOL", "RAN", 100), ("SOL", "PRX", 90), ("SOL", "SIR", 100),
        ("SOL", "ARC", 200), ("SOL", "ALD", 250), ("PRX", "SOL", 90),
        ("PRX", "SIR", 100), ("PRX", "ALT", 150), ("SIR", "SOL", 80),
        ("SIR", "PRX", 10), ("SIR", "CAS", 200), ("CAS", "SIR", 200),
        ("CAS", "PRO", 80), ("PRO", "CAS", 80), ("DEN", "PRO", 5),
        ("DEN", "ARC", 2), ("DEN", "FOM", 8), ("DEN", "RAN", 100),
        ("DEN", "ALD", 3), ("RAN", "SOL", 100), ("ARC", "SOL", 500),
        ("ARC", "DEN", 120), ("FOM", "PRX", 10), ("FOM", "DEN", 20),
        ("FOM", "ALS", 9), ("ALT", "FOM", 140), ("ALT", "VEG", 220),
        ("VEG", "ARC", 220), ("VEG", "ALD", 580), ("ALD", "SOL", 200),
        ("ALD", "ALS", 160), ("ALD", "VEG", 320), ("ALS", "ALT", 1),
        ("ALS", "ALD", 1)
    ]

    # Insert routes into the database
    for source, destination, hu in routes_data:
        if source in gates and destination in gates:
            route = Route(
                source_gate_id=gates[source].id,
                destination_gate_id=gates[destination].id,
                hyperplane_units=hu
            )
            db.session.add(route)
        else:
            print(f"Warning: Either {source} or {destination} does not exist in the database!")

    db.session.commit()
    print("✅ Routes seeded successfully!")

