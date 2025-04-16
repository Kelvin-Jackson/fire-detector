
#  Fire Detection System – ML + Flask + PostgreSQL + Docker

This project is a machine learning-based fire detection system powered by Flask, PostgreSQL, Docker, and Mage AI. The backend supports model training, prediction APIs, and data processing.



##  Running the Application with Docker

###  Build and Start the Application
```bash
docker compose up --build -d
```



###  Check Running Services
```bash
docker ps
```



###  Stop All Containers
```bash
docker compose down
```



###  Port Forwarding

After starting the application:

1. Head to the **Ports** tab in your Docker environment.
2. Ensure the following ports are forwarded:
   - **Port `5000`** – for the Flask application.
   - **Port `6789`** – for Mage AI.





##  Environment Setup

Make sure your `.env` file contains the correct environment variables:

```env
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_host
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
SECRET_KEY=your_secret_key
```



## 🧪 Testing the Prediction API

Once your app is running, send a POST request to:
```
http://localhost:5000/predict
```

Example payload:
```json
{
  "sensor_timestamp": "2025-04-15T14:30:00",
  "modis_timestamp": "2025-04-15T14:00:00",
  "fire_lat": -1.286389,
  "fire_long": 36.817223,
  "bright_ti4": 300.12,
  "fire_radiative_power": 25.0,
  "confidence": "high",
  "daynight": "D"
}
```




pgcli -h 127.0.0.1 -d magic -u root -p 5432



SELECT json_agg(prediction_data) AS data
FROM prediction_data;
