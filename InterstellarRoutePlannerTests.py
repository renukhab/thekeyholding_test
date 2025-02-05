import unittest
from app import app, db
from models import Gate, Route

class InterstellarRoutePlannerTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://renukha:password@localhost:5432/interstellar_routes"
        
        with app.app_context():
            db.create_all()  # Ensure tables exist
    
    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()  # Close the session properly
    
    def test_get_all_gates(self):
        response = self.client.get('/api/gates')
        self.assertEqual(response.status_code, 200)
        self.assertIn('SOL', response.get_data(as_text=True))
    
    def test_get_single_gate(self):
        response = self.client.get('/api/gates/SOL')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Sol', response.get_data(as_text=True))
    
    def test_get_invalid_gate(self):
        response = self.client.get('/api/gates/XYZ')
        self.assertEqual(response.status_code, 404)
    
    def test_transport_cost(self):
        response = self.client.get('/api/transport/1.0?passengers=3&parking=2')  # Use float for better route matching
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('cheapest', json_data)
        self.assertIn('cost', json_data)
    
    def test_nearest_gate(self):
        response = self.client.get('/api/nearest-gate/1.0')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('nearest_gate', json_data)
    
    def test_shortest_route_exists(self):
        response = self.client.get('/api/gates/SOL/to/ALT')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('route', json_data)
        self.assertEqual(json_data['route'], ['SOL', 'PRX', 'ALT'])
    
    def test_no_route_available(self):
        response = self.client.get('/api/gates/SOL/to/XYZ')
        self.assertEqual(response.status_code, 404)
    
    def test_one_way_route(self):
        response = self.client.get('/api/gates/ALT/to/SOL')
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_distance_for_transport(self):
        response = self.client.get('/api/transport/-1?passengers=3&parking=2')
        self.assertEqual(response.status_code, 404)
    
    def test_invalid_input_for_route(self):
        response = self.client.get('/api/gates/123/to/456')
        self.assertEqual(response.status_code, 404)
    
if __name__ == '__main__':
    unittest.main()
