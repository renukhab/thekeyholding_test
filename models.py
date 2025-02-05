from database import db
from sqlalchemy.dialects.postgresql import JSON

class Gate(db.Model):
    __tablename__ = "gate"

    id = db.Column(db.String(3), primary_key=True)  # 3-character ID
    name = db.Column(db.String(20), nullable=False)
    connections = db.Column(JSON, nullable=True)  # Store connections as JSON

    def __repr__(self):
        return f"<Gate {self.id} - {self.name}>"

class Route(db.Model):
    __tablename__ = "routes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_gate_id = db.Column(db.String(3), db.ForeignKey("gate.id"), nullable=False)
    destination_gate_id = db.Column(db.String(3), db.ForeignKey("gate.id"), nullable=False)
    hyperplane_units = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Route {self.source_gate_id} -> {self.destination_gate_id} ({self.hyperplane_units} HU)>"
