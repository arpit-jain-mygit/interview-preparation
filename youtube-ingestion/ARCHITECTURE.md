# Pipeline Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    YouTube Transcript Ingestion Pipeline              │
└─────────────────────────────────────────────────────────────────────┘

                          ╔═════════════════╗
                          ║ YouTube Channels║
                          ║  (Jain Content) ║
                          ╚════════┬════════╝
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │   Monitor Agent          │
                    │  (6 AM & 6 PM IST)       │
                    │  - Check channels       │
                    │  - Find new videos      │
                    └──────────┬───────────────┘
                               │ (Video IDs)
                               ▼
                    ┌──────────────────────────┐
                    │   SQLite Database        │
                    │  ┌────────────────────┐  │
                    │  │ videos table       │  │  Stores:
                    │  │ jobs table         │  │  - Found videos
                    │  │ monitoring_log     │  │  - Job status
                    │  └────────────────────┘  │  - Error tracking
                    └──────────┬───────────────┘
                               │ (Pending Jobs)
                               ▼
                    ┌──────────────────────────┐
                    │   Process Agent          │
                    │  (Every 5 minutes)       │
                    │  - Get pending jobs     │
                    │  - Download transcripts │
                    │  - Save to folder       │
                    └──────────┬───────────────┘
                               │ (Transcript Files)
                               ▼
                    ┌──────────────────────────┐
                    │   Output Folder          │
                    │  transcripts/            │
                    │  ├── channel_id_1/      │
                    │  │   ├── video_1.json   │
                    │  │   ├── video_1.txt    │
                    │  │   └── ...             │
                    │  └── channel_id_2/      │
                    │      └── ...             │
                    └──────────────────────────┘
```

## Component Details

### 1. Monitor Agent (`monitor_agent.py`)

**Purpose:** Discovers new videos on YouTube channels

**How it works:**
1. Runs on schedule (6 AM & 6 PM IST)
2. Queries YouTube API for each channel
3. Gets last 50 videos from uploads playlist
4. Records new videos in database
5. Creates processing job for each new video

**Input:** Channel IDs from `config.py`
**Output:** Job records in `jobs` table

### 2. Process Agent (`process_agent.py`)

**Purpose:** Downloads transcripts and saves them

**How it works:**
1. Polls database every 5 minutes
2. Gets pending jobs (videos not yet processed)
3. Downloads transcript from YouTube
4. Saves in two formats: JSON & TXT
5. Updates job status: pending → processing → completed/failed

**Input:** Pending jobs from database
**Output:** Transcript files on disk

### 3. Database (`database.py`)

**Purpose:** Tracks all videos and processing state

**Tables:**

| Table | Purpose |
|-------|---------|
| `videos` | Records all discovered videos |
| `jobs` | Tracks processing state of each video |
| `monitoring_log` | History of monitoring checks |

**Why SQLite?**
- Zero setup (file-based)
- Handles concurrent reads well
- Perfect for small-to-medium scale
- Easy backup (just copy file)

### 4. Scheduler (`scheduler.py`)

**Purpose:** Orchestrates when agents run

**Tasks:**
- **Morning Check**: 6 AM IST → Monitor Agent
- **Evening Check**: 6 PM IST → Monitor Agent  
- **Continuous Processing**: Every 5 minutes → Process Agent

**Why APScheduler?**
- Reliable task scheduling
- Timezone-aware (handles IST)
- No external dependencies
- Runs in single process

### 5. CLI (`cli.py`)

**Purpose:** Management and monitoring interface

**Commands:**
- `monitor` - Run monitor manually
- `process` - Run processor manually
- `start` - Start full scheduler
- `jobs` - List recent jobs
- `stats` - View pipeline statistics
- `job-detail` - Get specific job info
- `config` - Show configuration

## Data Flow

### New Video Discovery

```
1. Monitor Agent runs at scheduled time
   ↓
2. YouTube API → list recent videos on channel
   ↓
3. Check if video_id already in videos table
   ↓
4. If new → insert into videos table
   ↓
5. Create job record with status=pending
   ↓
6. Log the monitoring check
```

### Transcript Processing

```
1. Process Agent polls jobs table
   ↓
2. Find jobs with status=pending
   ↓
3. Update status to processing
   ↓
4. YouTube Transcript API → get captions
   ↓
5. Save to transcripts/ folder
   ↓
6. Update job status to completed
   ↓
7. (If error → status=failed with error message)
```

## Concurrency & Safety

### Database Locking
- SQLite uses file-level locking
- Works fine with multiple readers
- Single writer at a time (acceptable here)

### Job State Machine
```
         ┌─────────────┐
         │   PENDING   │
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │ PROCESSING  │
         └──┬────────┬─┘
            │        │
        Success   Failure
            │        │
            ▼        ▼
         ┌──────┐  ┌───────┐
         │      │  │       │
      COMPLETED FAILED
         │      │  │       │
         └──────┘  └───────┘
            Final States
```

### Duplicate Prevention
- Video primary key prevents re-insertion
- Job created only for new videos
- Processing idempotent (re-downloading same video is safe)

## Error Handling

### Monitor Agent Failures
```
Try get channel videos
    ↓ (fail)
Log error + continue to next channel
Log failure in monitoring_log
No jobs created (video not recorded)
Pipeline continues
```

### Process Agent Failures
```
Try download transcript
    ↓ (fail)
Job status → FAILED
Error message stored in database
Process agent continues with next job
Can retry manually or automatically
```

## Configuration Points

| Setting | Location | Impact |
|---------|----------|--------|
| Channels to monitor | `config.py` CHANNELS | What videos we find |
| Check schedule | `config.py` MORNING/EVENING_CHECK_TIME | When monitor runs |
| Process frequency | `scheduler.py` add_job interval | How fast we download |
| Output folder | `config.py` OUTPUT_FOLDER | Where transcripts go |
| Database path | `config.py` DB_PATH | Where to store state |
| API key | `.env` YOUTUBE_API_KEY | YouTube API access |

## Scaling Considerations

### Small Scale (5-10 channels)
- Current architecture perfect
- SQLite fully sufficient
- No optimization needed

### Medium Scale (10-50 channels)
- Monitor may take a few seconds per channel
- Process agent handles fine
- Consider increasing processing frequency

### Large Scale (50+ channels)
- Monitor becomes bottleneck
- Consider:
  - Batch YouTube API calls
  - Move monitor to separate process
  - Use PostgreSQL instead of SQLite
  - Add multiple processor instances

### Very Large Scale (1000+ channels)
- Full distributed architecture needed
- See DEPLOYMENT.md for cloud options
- Message queue instead of database polling
- Distributed processing

## Future Enhancements

1. **Webhook Integration**
   - POST to doc-transcribe API immediately
   - Trigger downstream processing

2. **Retry Logic**
   - Exponential backoff for failed jobs
   - Max retry count

3. **Caching**
   - Cache channel metadata
   - Reduce API calls

4. **Monitoring & Alerting**
   - Dashboard of pipeline health
   - Alert on failures
   - Metrics export (Prometheus)

5. **Advanced Filtering**
   - Only download certain video lengths
   - Language filtering
   - Publish date filtering

6. **Transcript Enhancement**
   - Speaker identification
   - Timestamp alignment
   - NLP processing (entities, topics)

7. **Multi-Language Support**
   - Download in multiple languages
   - Auto-translation

## External Dependencies

| Package | Purpose | License |
|---------|---------|---------|
| google-api-python-client | YouTube API | Apache 2.0 |
| youtube-transcript-api | Download transcripts | MIT |
| apscheduler | Task scheduling | MIT |
| pytz | Timezone handling | MIT |
| python-dotenv | .env file loading | BSD |
| click | CLI framework | BSD |
| tabulate | Pretty tables | MIT |

All have permissive licenses suitable for commercial use.
