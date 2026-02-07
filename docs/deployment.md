# AI Post-Graduate Entrance Exam Platform Deployment Documentation

## 1. Prerequisites
- Docker Engine (v20.10+)
- Docker Compose (v2.0+)
- Git

## 2. Architecture
The system consists of the following containers:
- **frontend**: Vue 3 application served by Nginx
- **backend**: FastAPI application
- **crawler**: Scrapy spider
- **db**: PostgreSQL database
- **redis**: Redis cache

## 3. Deployment Steps

### Step 1: Clone the repository
```bash
git clone <repository_url>
cd <project_directory>
```

### Step 2: Build and Run Containers
```bash
docker-compose up -d --build
```
This command will build all images and start the services in detached mode.

### Step 3: Initialize Database
Once the containers are running, you need to populate the database with initial data (50 universities).

```bash
docker-compose exec backend python -m app.init_data
```

### Step 4: Verify Deployment
- **Frontend**: Access http://localhost:3000
- **Backend API Docs**: Access http://localhost:8000/docs
- **Database**: Port 5432 is exposed
- **Redis**: Port 6379 is exposed

## 4. Maintenance

### View Logs
```bash
docker-compose logs -f [service_name]
```

### Stop Services
```bash
docker-compose down
```

### Run Crawler Manually
```bash
docker-compose exec crawler scrapy crawl edu_spider
```

## 5. Stress Testing
To run stress tests using Locust:

1. Install Locust locally: `pip install locust`
2. Run Locust: `locust -f tests/locustfile.py`
3. Open http://localhost:8089 in your browser and start the test.
