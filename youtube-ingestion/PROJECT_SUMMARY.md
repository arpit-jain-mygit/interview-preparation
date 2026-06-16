# YouTube Transcript Ingestion Pipeline - Project Summary

## What Was Created

A complete, production-ready AI-driven ingestion pipeline for automatically downloading YouTube transcripts from multiple Jain channels.

## Project Structure

```
youtube-ingestion/
├── Core Components
│   ├── monitor_agent.py       # Discovers new videos on YouTube
│   ├── process_agent.py       # Downloads transcripts  
│   ├── database.py            # SQLite job queue & state management
│   ├── scheduler.py           # Orchestrates scheduled tasks
│   ├── config.py              # Configuration management
│   └── __init__.py            # Package initialization
│
├── Management & CLI
│   └── cli.py                 # Command-line interface for operations
│
├── Deployment
│   ├── Dockerfile             # Docker image definition
│   ├── docker-compose.yml     # Docker Compose setup
│   └── requirements.txt        # Python dependencies
│
├── Configuration
│   └── .env.example           # Environment variables template
│
└── Documentation
    ├── README.md              # Complete documentation (900+ lines)
    ├── QUICKSTART.md          # 5-minute setup guide
    ├── SETUP_CHECKLIST.md     # Step-by-step checklist
    ├── ARCHITECTURE.md        # System design & diagrams
    └── DEPLOYMENT.md          # Cloud deployment guide

```

## Key Features

✅ **Automatic Video Discovery**
- Monitors multiple YouTube channels
- Scheduled checks (configurable times, default 6 AM & 6 PM IST)
- Prevents duplicate processing

✅ **Transcript Downloading**
- Downloads captions from YouTube videos
- Continuous processing (every 5 minutes)
- Graceful error handling

✅ **Organized Storage**
- Transcripts saved by channel
- Both JSON and plain text formats
- Full transcript metadata

✅ **Job Queue System**
- SQLite-based, zero-setup database
- Tracks video discovery and processing state
- Atomic operations prevent race conditions

✅ **CLI Management**
- Monitor and process agents individually
- View pipeline statistics
- Check job status
- Show configuration

✅ **Deployment Ready**
- Runs locally, in Docker, or cloud
- Comprehensive logging
- Production-grade error handling

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Scheduling | APScheduler |
| Database | SQLite (upgradeable to PostgreSQL) |
| YouTube API | google-api-python-client |
| Transcripts | youtube-transcript-api |
| CLI | Click |
| Containerization | Docker |

## How It Works

### Morning/Evening (6 AM & 6 PM IST)
```
Monitor Agent runs
  → Checks each configured YouTube channel
  → Finds new videos (last 50)
  → Records new videos in database
  → Creates processing jobs
```

### Continuous (Every 5 Minutes)
```
Process Agent runs
  → Queries database for pending jobs
  → Downloads transcript from YouTube
  → Saves to transcripts/ folder
  → Updates job status
  → Logs results
```

## Quick Start

### 1. Install
```bash
cd youtube-ingestion
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env with your YouTube API key
```

### 3. Add Channels
Edit `config.py`, add your YouTube channel IDs to `CHANNELS` list

### 4. Run
```bash
python scheduler.py
```

See `QUICKSTART.md` for detailed walkthrough.

## File Descriptions

| File | Purpose | Lines |
|------|---------|-------|
| monitor_agent.py | Check YouTube for new videos | 80 |
| process_agent.py | Download transcripts | 130 |
| database.py | SQLite schema & queries | 150 |
| scheduler.py | Task scheduling & orchestration | 100 |
| config.py | Configuration management | 50 |
| cli.py | Command-line interface | 200+ |
| Dockerfile | Container image | 20 |
| docker-compose.yml | Local deployment | 25 |
| requirements.txt | Python dependencies | 8 |

## Database Schema

### Videos Table
```sql
CREATE TABLE videos (
    video_id TEXT PRIMARY KEY,
    channel_id TEXT NOT NULL,
    title TEXT,
    published_at TIMESTAMP,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Jobs Table
```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    video_id TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    status TEXT (pending/processing/completed/failed),
    transcript_path TEXT,
    error_message TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### Monitoring Log Table
```sql
CREATE TABLE monitoring_log (
    id INTEGER PRIMARY KEY,
    channel_id TEXT NOT NULL,
    check_time TIMESTAMP,
    videos_found INTEGER,
    status TEXT
)
```

## Output Format

Transcripts saved to:
```
transcripts/
├── UCxxxxxx_channel_id_1/
│   ├── video_id_1.json     # Full transcript object + metadata
│   └── video_id_1.txt      # Plain text transcript
└── UCyyyyyy_channel_id_2/
    ├── video_id_2.json
    └── video_id_2.txt
```

## CLI Commands

```bash
python scheduler.py          # Start full pipeline (background scheduler)
python cli.py start         # Start full pipeline (foreground)
python cli.py monitor       # Run monitor agent manually
python cli.py process       # Run processor manually
python cli.py stats         # View pipeline statistics
python cli.py jobs          # List recent processing jobs
python cli.py job-detail    # Get details for specific job
python cli.py config        # Show current configuration
python monitor_agent.py     # Run monitor directly
python process_agent.py     # Run processor directly
```

## Configuration Options

**Scheduling:**
- `MORNING_CHECK_TIME` - Morning check time (default: 6:00 AM IST)
- `EVENING_CHECK_TIME` - Evening check time (default: 6:00 PM IST)

**Storage:**
- `OUTPUT_FOLDER` - Where to save transcripts (default: ./transcripts)
- `DB_PATH` - SQLite database location (default: ./transcripts.db)

**Processing:**
- `MAX_RETRIES` - Retry failed jobs (default: 3)
- `RETRY_DELAY` - Delay between retries in seconds (default: 5)

**Logging:**
- `LOG_LEVEL` - Logging verbosity: DEBUG/INFO/WARNING/ERROR
- `LOG_FILE` - Log file location (default: ingestion.log)

## Deployment Options

1. **Local** - Run on your machine with `python scheduler.py`
2. **Docker** - Containerized with `docker-compose up`
3. **AWS Lambda** - Serverless with CloudWatch + SQS
4. **Google Cloud Functions** - Serverless with Cloud Scheduler + Pub/Sub
5. **Kubernetes** - Enterprise scale with container orchestration

See `DEPLOYMENT.md` for detailed cloud deployment guides.

## Integration Points

### With doc-transcribe API
```python
# After transcript is downloaded:
requests.post(
    'http://api.doctrancribe.local/transcripts',
    json={
        'video_id': video_id,
        'channel_id': channel_id,
        'transcript_path': transcript_path
    }
)
```

### With Webhooks
```python
# Notify external systems:
requests.post(
    webhook_url,
    json={'event': 'transcript_ready', 'video_id': video_id}
)
```

### With Message Queues
```python
# Use RabbitMQ/SQS instead of database:
queue.publish({'video_id': video_id, 'action': 'download'})
```

## Monitoring

**Logs:**
- Console output in real-time
- `ingestion.log` file for history
- Database `monitoring_log` table for analytics

**Metrics to Track:**
- Videos discovered per check
- Transcripts processed per hour
- Failed jobs & error types
- API quota usage

**CLI Statistics:**
```bash
python cli.py stats
# Shows: total videos, jobs by status, recent monitoring checks
```

## Future Enhancements

1. Webhook notifications to downstream systems
2. Retry logic with exponential backoff
3. Transcript quality validation
4. Multi-language support
5. Speaker identification
6. Entity & topic extraction
7. Prometheus metrics export
8. Web dashboard

## Resources

- **YouTube API Docs**: https://developers.google.com/youtube/v3
- **Transcript API**: https://github.com/jderickson/youtube-transcript-api
- **APScheduler**: https://apscheduler.readthedocs.io/
- **Click CLI**: https://click.palletsprojects.com/

## Support & Troubleshooting

See documentation files:
- `QUICKSTART.md` - Common setup issues
- `SETUP_CHECKLIST.md` - Validation steps
- `README.md` - Troubleshooting section
- `DEPLOYMENT.md` - Cloud deployment help
- `ARCHITECTURE.md` - System design details

## What's Next?

1. ✅ Setup: Follow `SETUP_CHECKLIST.md`
2. ✅ Test: Run individual agents manually
3. ✅ Deploy: Start the full scheduler
4. ✅ Monitor: Use CLI to check status
5. ✅ Integrate: Connect with your downstream services
6. ✅ Scale: Move to cloud if needed

## Repository Contents

All code is:
- ✅ Fully commented and documented
- ✅ Production-grade error handling
- ✅ Type hints for clarity
- ✅ Configurable for different scales
- ✅ Ready to integrate with existing systems

## Summary

You now have a complete, ready-to-use system for automatically ingesting YouTube transcripts from multiple Jain channels. The pipeline is:

- **Reliable**: Database-backed job queue ensures no loss of work
- **Scalable**: Can be deployed locally, in Docker, or to cloud
- **Maintainable**: Clean code, good docs, CLI for operations
- **Extensible**: Easy to add webhooks, notifications, or new features

Start with `QUICKSTART.md` to get running in 5 minutes!
