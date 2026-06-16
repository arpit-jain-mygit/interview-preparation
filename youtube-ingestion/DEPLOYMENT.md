# Deployment Guide

## Local Deployment

### System Requirements
- Python 3.8+
- 100MB disk space for database and transcripts
- Internet access to YouTube API

### Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your YouTube API key
   ```

3. **Add channels**
   - Edit `config.py` and add your channel IDs

4. **Run**
   ```bash
   python scheduler.py
   ```

Keep running in the background using:
- `nohup python scheduler.py > ingestion.log 2>&1 &`
- `tmux` or `screen`
- systemd service
- Supervisor

## Docker Deployment

### Build and Run

```bash
# Build image
docker build -t youtube-ingestion:latest .

# Run container
docker run -d \
  -e YOUTUBE_API_KEY=your_key \
  -v $(pwd)/transcripts:/app/transcripts \
  -v $(pwd)/transcripts.db:/app/transcripts.db \
  --name youtube-ingestion \
  youtube-ingestion:latest

# View logs
docker logs -f youtube-ingestion

# Stop
docker stop youtube-ingestion
```

### Using Docker Compose

```bash
# Set your API key
export YOUTUBE_API_KEY=your_key

# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Cloud Deployment Options

### AWS Lambda + SQS

**Architecture:**
- Lambda function for monitor (CloudWatch trigger)
- SQS queue for jobs
- Lambda function for processor (SQS trigger)
- S3 for transcript storage

**Benefits:**
- Serverless (no servers to manage)
- Pay only for execution
- Auto-scaling
- Built-in monitoring

**Implementation:**
1. Create Lambda functions for monitor and process
2. Set CloudWatch events for 6 AM & 6 PM IST
3. Use SQS for job queue instead of SQLite
4. Store transcripts in S3
5. Use DynamoDB for job tracking

### Google Cloud Functions + Pub/Sub

**Architecture:**
- Cloud Function for monitor (Cloud Scheduler trigger)
- Pub/Sub topic for events
- Cloud Function for processor (Pub/Sub trigger)
- Cloud Storage for transcripts

**Benefits:**
- Simple deployment
- Integrated monitoring
- Pay per invocation
- Good for Python workloads

**Implementation:**
1. Deploy functions to Cloud Functions
2. Use Cloud Scheduler for timing
3. Use Pub/Sub for event messaging
4. Store transcripts in Cloud Storage
5. Use Firestore for job tracking

### Kubernetes (EKS/GKE)

For large-scale deployments (100+ channels):

```bash
# Build and push image
docker build -t gcr.io/project/youtube-ingestion:latest .
docker push gcr.io/project/youtube-ingestion:latest

# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml
```

**Benefits:**
- Handles large workloads
- Built-in orchestration
- Rolling updates
- Service discovery

## Configuration for Scale

### For 5-50 channels
- Local SQLite is fine
- Check every 5-10 minutes
- Single processor instance

### For 50-500 channels
- Move to PostgreSQL
- Check every 1-2 minutes
- 2-3 processor instances
- Consider Redis cache

### For 500+ channels
- Use managed database (RDS, Cloud SQL)
- Distributed processing (Celery, Airflow)
- Message queue (RabbitMQ, Kafka, SQS)
- Monitoring (DataDog, New Relic)

## Environment Variables

```
# Required
YOUTUBE_API_KEY          API key from Google Cloud Console

# Optional
DB_PATH                  Path to SQLite database (default: transcripts.db)
OUTPUT_FOLDER            Where to save transcripts (default: ./transcripts)
LOG_LEVEL                DEBUG|INFO|WARNING|ERROR (default: INFO)
```

## Database Migration (Local → Cloud)

### From SQLite to PostgreSQL

1. **Backup SQLite data**
   ```bash
   sqlite3 transcripts.db ".dump" > backup.sql
   ```

2. **Create PostgreSQL instance**
   - Create RDS instance or use managed service
   - Create database and tables

3. **Update config.py**
   ```python
   import psycopg2
   # Change database initialization
   ```

4. **Migrate data**
   - Scripts to convert SQLite to PostgreSQL schema
   - Bulk insert data

## Monitoring

### Key Metrics

- **Videos discovered per check** - Trending up/down?
- **Transcripts processed per hour** - Speed degradation?
- **Failed jobs** - Any patterns?
- **Processing latency** - How long to process?
- **API quota usage** - YouTube API calls per day

### Logging

- All logs go to `ingestion.log`
- Docker: `docker logs youtube-ingestion`
- Cloud: CloudWatch (AWS), Cloud Logging (GCP)
- Local: Parse ingestion.log with ELK or similar

### Health Checks

```bash
# Quick status check
python cli.py stats

# Verify database integrity
sqlite3 transcripts.db "SELECT COUNT(*) FROM videos;"
```

## Troubleshooting

### High Latency
- Increase processing frequency (reduce interval)
- Add more processor instances
- Check YouTube API rate limits

### Memory Issues
- Monitor job queue size
- Add batch processing limits
- Use pagination for channel queries

### Stuck Jobs
- Implement job timeout
- Auto-retry with backoff
- Manual intervention script

## Costs

### YouTube API
- Free: 10,000 quota units/day
- Each channel check: ~1-2 units
- Transcript download: ~1 unit

### AWS Lambda
- First 1M requests free
- $0.20 per 1M requests after
- Plus S3 storage costs

### GCP Cloud Functions
- First 2M invocations free
- $0.40 per 1M invocations after

## Maintenance

### Daily
- Monitor ingestion.log for errors
- Check dashboard/CLI for job queue size

### Weekly
- Review failed jobs
- Check API quota usage
- Verify transcript quality

### Monthly
- Backup database
- Review and optimize channels list
- Update dependencies
