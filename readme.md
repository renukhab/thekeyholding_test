# 🚀 Interstellar Route Planner API

![Flask](https://img.shields.io/badge/Flask-2.0-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-green.svg)
![Swagger](https://img.shields.io/badge/Swagger-OpenAPI-yellow.svg)

## 📌 **Project Overview**
The **Interstellar Route Planner API** helps calculate the most efficient routes between hyperspace gates and estimates transport costs. It provides endpoints for:
- Retrieving available gates
- Calculating travel costs
- Finding the shortest path between two gates

---

## 📑 **Table of Contents**
- [🛠️ Installation](#installation)
- [🚀 Running the API](#running-the-api)
- [🔌 API Endpoints](#api-endpoints)
- [📖 Swagger Documentation](#swagger-documentation)
- [☁️ Deployment on AWS EC2](#deployment-on-aws-ec2)
- [📜 License](#license)

---

## 🛠️ **Installation**

### **1️⃣ Clone the Repository**
```bash
 git clone https://github.com/your-username/interstellar-route-planner.git
 cd interstellar-route-planner
```

### **2️⃣ Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip3 install -r requirements.txt
```

### **4️⃣ Set Up PostgreSQL Database**
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo -u postgres psql
sudo pg_dump -U myuser -h localhost -d interstellar_routes -f create-local-postgres-db.sql
```
Inside PostgreSQL shell:
```sql
CREATE DATABASE interstellar_routes;
CREATE USER myuser WITH ENCRYPTED PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE interstellar_routes TO myuser;
\q
```

---

## 🚀 **Running the API**

### **1️⃣ Set Environment Variables**
```bash
export FLASK_APP=app.py  # For Linux/macOS
set FLASK_APP=app.py      # For Windows (CMD)
$env:FLASK_APP="app.py"   # For PowerShell
```

### **2️⃣ Run Database Migrations**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### **3️⃣ Start the Flask API**
```bash
flask run --host=0.0.0.0 --port=5000
```

The API will be available at:
```
http://127.0.0.1:5000/api/
```

---

## 🔌 **API Endpoints**

| Method | Endpoint | Description |
|--------|-------------|-------------|
| **GET** | `/api/gates` | Get a list of all gates |
| **GET** | `/api/gates/{gateCode}` | Get details of a specific gate |
| **GET** | `/api/gates/{gateCode}/to/{targetGateCode}` | Find the cheapest route between two gates |
| **GET** | `/api/transport/{distance}?passengers={num}&parking={days}` | Calculate the cheapest transport cost |

---

## 📖 **Swagger Documentation**

Swagger UI is available at:
```
http://127.0.0.1:5000/api/swagger-ui/
```
To view raw OpenAPI JSON:
```
http://127.0.0.1:5000/api/swagger.json
```

---

## ☁️ **Deployment on AWS EC2**

### **1️⃣ Launch an EC2 Instance**
- Choose **Ubuntu 22.04 LTS**
- Open required ports (22 for SSH, 5000 for API, 80 for web access)

### **2️⃣ Connect to the EC2 Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### **3️⃣ Install Dependencies on EC2**
```bash
sudo apt update && sudo apt install python3-pip python3-venv git nginx -y
```

### **4️⃣ Clone and Set Up Project on EC2**
```bash
git clone https://github.com/your-username/interstellar-route-planner.git
cd interstellar-route-planner
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **5️⃣ Start Flask as a Background Process**
```bash
pip install gunicorn
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app &
```

### **6️⃣ Configure Nginx Reverse Proxy**
```bash
sudo nano /etc/nginx/sites-available/flaskapp
```
Paste this config:
```
server {
    listen 80;
    server_name your-ec2-public-ip;
    location / {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
Save & apply:
```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

Your API is now live at:
```
http://your-ec2-public-ip
```
