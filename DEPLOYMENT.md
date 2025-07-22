# 🚀 Deployment Guide - Solar AI Agent Dashboard

This guide covers all deployment options for the Solar AI Agent Dashboard - a professional AI agent management platform.

## 📋 Prerequisites

- **Node.js 20+**
- **Python 3.11+**
- **Redis** (for real-time features)
- **PostgreSQL** (for data persistence)
- **Docker** (for containerized deployments)
- **pnpm** (recommended package manager)
- **uv** (Python package manager)

## 🔧 Environment Configuration

### Frontend Environment Variables

Create `app/.env` file:
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_APP_TITLE="Solar AI Agent Dashboard"
VITE_APP_VERSION=1.0.0

# Real-time Features
VITE_ENABLE_REAL_TIME=true
VITE_WS_RECONNECT_INTERVAL=5000
VITE_METRICS_UPDATE_INTERVAL=5000

# Dashboard Configuration
VITE_MAX_AGENTS_DISPLAY=100
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false

# Theme Configuration
VITE_DEFAULT_THEME=dark
VITE_ENABLE_THEME_SWITCHING=true
```

### Backend Environment Variables

Create `services/.env` file:
```env
# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1
LOG_LEVEL=info

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/agents_db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Agent Management
MAX_AGENTS_PER_USER=50
AGENT_HEALTH_CHECK_INTERVAL=30
AGENT_METRICS_RETENTION_DAYS=90

# Real-time Features
WS_PING_INTERVAL=20
WS_PING_TIMEOUT=10
BROADCAST_INTERVAL=5

# External Services
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
PROMETHEUS_ENDPOINT=http://localhost:9090
```

## 🐳 Docker Deployment Options

### E2B Platform Deployment

**E2B** provides development environments with Redis and multi-service support.

```bash
# Build E2B image
docker build -f e2b.Dockerfile -t solar-agent-dashboard:e2b .

# Run E2B container with all services
docker run -p 5173:5173 -p 8000:8000 -p 6379:6379 solar-agent-dashboard:e2b
```

**E2B Features:**
- Multi-service container (Frontend + Backend + Redis)
- Real-time WebSocket support
- Agent health monitoring
- Development-optimized with hot reload

### Production Docker Compose

```bash
# Full production environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build

# Development environment
docker-compose up --build
```

**Services Included:**
- Frontend (React dashboard)
- Backend (FastAPI with WebSocket)
- Redis (Real-time data)
- PostgreSQL (Agent data persistence)
- Nginx (Load balancing and SSL)

## 🔄 Local Development Setup

### Option 1: Manual Setup

**1. Database Setup:**
```bash
# Install and start Redis
brew install redis  # macOS
sudo apt install redis-server  # Ubuntu
redis-server

# Install and start PostgreSQL
brew install postgresql  # macOS
sudo apt install postgresql  # Ubuntu
psql -c "CREATE DATABASE agents_db;"
```

**2. Frontend Setup:**
```bash
cd app
pnpm install
pnpm dev
```

**3. Backend Setup:**
```bash
cd services
uv sync

# Run database migrations
uv run alembic upgrade head

# Start the server
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker Development

```bash
# Start all services with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Platform Deployments

### Railway (Recommended for Production)

1. **Connect Repository:**
   - Link GitHub repository to Railway
   - Railway auto-detects multiple services

2. **Configure Services:**
   ```yaml
   # railway.toml
   [build]
   builder = "DOCKERFILE"
   dockerfilePath = "railway.Dockerfile"
   
   [deploy]
   startCommand = "/deployment/start.sh"
   restartPolicyType = "ON_FAILURE"
   
   [[services]]
   name = "dashboard-frontend"
   source = "app"
   
   [[services]]
   name = "dashboard-backend"
   source = "services"
   
   [[services]]
   name = "redis"
   image = "redis:7-alpine"
   
   [[services]]
   name = "postgres"
   image = "postgres:15"
   ```

3. **Environment Variables:**
   ```env
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   SECRET_KEY=${{RAILWAY_SECRET_KEY}}
   OPENAI_API_KEY=${{OPENAI_API_KEY}}
   ```

### AWS/GCP/Azure Deployment

**Container Services:**
- **AWS ECS/Fargate**: Container orchestration
- **GCP Cloud Run**: Serverless containers
- **Azure Container Instances**: Managed containers

**Required Services:**
- **Database**: AWS RDS / GCP Cloud SQL / Azure Database
- **Cache**: AWS ElastiCache / GCP Memorystore / Azure Cache
- **Load Balancer**: Application Load Balancer
- **SSL**: Certificate Manager for HTTPS

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-dashboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-dashboard
  template:
    metadata:
      labels:
        app: agent-dashboard
    spec:
      containers:
      - name: dashboard
        image: ghcr.io/mikeschlottig/solar-ai-agent-dashboard:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: url
```

## 📊 Monitoring and Observability

### Application Monitoring

**Metrics Collection:**
```python
# Prometheus metrics endpoint
from prometheus_client import Counter, Histogram, Gauge

agent_requests = Counter('agent_requests_total', 'Total agent requests')
agent_response_time = Histogram('agent_response_seconds', 'Agent response time')
active_agents = Gauge('active_agents_total', 'Number of active agents')
```

**Health Checks:**
```bash
# Application health
curl http://localhost:8000/health

# Agent status
curl http://localhost:8000/api/agents/health

# Database connection
curl http://localhost:8000/health/db

# Redis connection
curl http://localhost:8000/health/redis
```

### Logging Configuration

**Structured Logging:**
```python
# services/logging_config.py
from loguru import logger

# Dashboard activities
logger.add(
    "logs/dashboard.log",
    format="{time} | {level} | {name}:{function} | {message}",
    rotation="1 day",
    retention="30 days"
)

# Agent activities
logger.add(
    "logs/agents.log",
    filter=lambda record: "agent_activity" in record["extra"],
    format="{time} | AGENT | {extra[agent_id]} | {message}",
    rotation="1 day",
    retention="90 days"
)
```

### Performance Optimization

**Frontend Optimizations:**
- Lazy loading for dashboard components
- Virtual scrolling for large agent lists
- WebSocket connection pooling
- Memoized chart components

**Backend Optimizations:**
- Connection pooling for database
- Redis caching for frequent queries
- Async processing for agent operations
- Background task queues with Celery

## 🔒 Security Configuration

### Authentication Setup

```python
# JWT Configuration
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60
JWT_REFRESH_EXPIRATION_DAYS = 7

# CORS Configuration
CORS_ORIGINS = [
    "https://yourdomain.com",
    "https://dashboard.yourdomain.com"
]

# Rate Limiting
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds
```

### Security Headers

```python
# FastAPI security middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.security import SecurityHeadersMiddleware

app.add_middleware(
    SecurityHeadersMiddleware,
    content_security_policy="default-src 'self'",
    x_frame_options="DENY",
    x_content_type_options="nosniff"
)
```

## 🚨 Troubleshooting

### Common Issues

**WebSocket Connection Failures:**
```bash
# Check WebSocket endpoint
wscat -c ws://localhost:8000/ws

# Verify Redis connection
redis-cli ping

# Check firewall rules
sudo ufw status
```

**Agent Health Check Failures:**
```bash
# Check agent logs
docker logs solar-agent-dashboard

# Verify database connectivity
psql $DATABASE_URL -c "SELECT 1;"

# Check system resources
docker stats
```

**Performance Issues:**
```bash
# Monitor resource usage
top -p $(pgrep -f "uvicorn")

# Check database performance
psql $DATABASE_URL -c "SELECT * FROM pg_stat_activity;"

# Monitor Redis memory
redis-cli info memory
```

### Log Analysis

```bash
# View dashboard logs
tail -f logs/dashboard.log

# Agent activity logs
grep "agent_activity" logs/agents.log

# Error analysis
grep "ERROR" logs/*.log | tail -20

# Performance metrics
grep "metrics" logs/dashboard.log | tail -10
```

## 📈 Scaling Considerations

### Horizontal Scaling

- **Load Balancer**: Nginx or cloud load balancer
- **Multiple Backend Instances**: Scale FastAPI workers
- **Database Sharding**: Partition agent data
- **Redis Clustering**: Scale real-time features

### Performance Monitoring

- **Response Times**: < 200ms for dashboard updates
- **WebSocket Latency**: < 100ms for real-time updates
- **Agent Health Checks**: 30-second intervals
- **Memory Usage**: < 512MB per backend instance

## 🎯 Next Steps

1. **Set up monitoring** with Prometheus and Grafana
2. **Configure alerting** for agent failures
3. **Implement backup strategy** for agent configurations
4. **Set up CI/CD pipeline** for automated deployments
5. **Configure SSL certificates** for production

---

**Need help?** Check the [README.md](README.md) or create an issue in the repository.

*Last updated: July 22, 2025*