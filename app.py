from flask import Flask
from flask_migrate import Migrate
from database import db
from models import Gate, Route
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://renukha:password@localhost/interstellar_routes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)  # Ensure Migrate is initialized
CORS(app)

# Import routes after initializing db to avoid circular import issues
from routes import api_blueprint
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=True)

