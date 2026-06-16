# YouTube Transcript Ingestion Pipeline

An AI-driven ingestion pipeline for automatically downloading transcripts from YouTube videos across multiple Jain channels.

## Architecture

The pipeline consists of three main components:

1. **Monitor Agent** - Checks configured YouTube channels for new videos (runs at configured IST times)
2. **Process Agent** - Downloads transcripts for newly discovered videos (runs continuously)
3. **Job Queue** - SQLite-based database tracks videos and processing jobs

### Flow

```
YouTube Channels → Monitor Agent → Job Queue (Database)
                                        ↓
                                   Process Agent → Output Folder
                                        ↓
                              transcript.json, transcript.txt
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create API credentials (API Key)
5. Copy the key

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:
```
YOUTUBE_API_KEY=your_key_here
OUTPUT_FOLDER=./transcripts
DB_PATH=./transcripts.db
LOG_LEVEL=INFO
```

### 4. Add Your Channels

Edit `config.py` and add your Jain channel IDs:

```python
CHANNELS: List[ChannelConfig] = [
    ChannelConfig(
        name="Channel Name",
        channel_id="UCxxxxxxxxxxxxxx",
        description="Description"
    ),
]
```

To find your channel ID:
- Go to the YouTube channel
- Copy the channel ID from the URL: `youtube.com/@channelname` or `youtube.com/channel/CHANNEL_ID`

## Usage

### Start the Full Pipeline

Runs monitor agent (morning & evening IST) and process agent (every 5 minutes):

```bash
python scheduler.py
```

The pipeline will:
- Check channels at 6 AM and 6 PM IST daily
- Process pending transcripts every 5 minutes
- Save transcripts to `OUTPUT_FOLDER` organized by channel

### Run Individual Agents

**Monitor only** (check for new videos):
```bash
python monitor_agent.py
```

**Process only** (download transcripts):
```bash
python process_agent.py
```

## Database Schema

### `videos` table
- `video_id` (PK): YouTube video ID
- `channel_id`: Channel that uploaded the video
- `title`: Video title
- `published_at`: Publication timestamp
- `discovered_at`: When we found it

### `jobs` table
- `job_id` (PK): Unique job identifier
- `video_id`: Associated video
- `status`: pending, processing, completed, failed
- `transcript_path`: Path to saved transcript (if completed)
- `error_message`: Error details (if failed)
- `created_at`, `updated_at`: Timestamps

### `monitoring_log` table
- Records of each monitoring run with success/failure status

## Output Structure

```
transcripts/
├── UCxxxxxxxxxxxxxx/  (channel_id)
│   ├── video_id_1.json
│   ├── video_id_1.txt
│   ├── video_id_2.json
│   ├── video_id_2.txt
│   └── ...
└── UCyyyyyyyyyyyyyyyy/
    ├── ...
```

Each transcript is saved in both:
- **JSON format**: Contains full transcript object and plain text
- **TXT format**: Plain text for easy reading

## Logging

Logs are written to:
- Console (stdout)
- `ingestion.log` file in the working directory

Check logs to monitor pipeline health:
```bash
tail -f ingestion.log
```

## Customization

### Change Monitor Schedule

Edit `config.py`:
```python
MORNING_CHECK_TIME = time(6, 0)  # Change to desired hour
EVENING_CHECK_TIME = time(18, 0)
```

### Change Processing Frequency

Edit `scheduler.py`:
```python
self.scheduler.add_job(
    self._process_task,
    'interval',
    minutes=5,  # Change this value
    ...
)
```

### Add More Channels

In `config.py`, add to `CHANNELS` list:
```python
ChannelConfig(
    name="New Channel",
    channel_id="UCxxxx...",
    description="..."
)
```

## Troubleshooting

### "YOUTUBE_API_KEY is not set"
- Ensure `.env` file exists with `YOUTUBE_API_KEY`
- Verify the environment variable is loaded

### "Transcripts are disabled"
- Some videos don't have transcripts available on YouTube
- Pipeline logs this and continues with next video

### "No transcript found"
- Auto-generated or unavailable transcripts
- Check YouTube directly to confirm transcript exists

### Database locked
- Another process is using the database
- Wait or stop other instances

## Next Steps

### Integration with doc-transcribe
Connect this pipeline to the existing `doc-transcribe-api`:
- POST new transcripts to the API
- Store transcript metadata
- Trigger additional processing (NLP, indexing, etc.)

### Add Webhook Notifications
Notify external systems of new transcripts via webhooks

### Add Error Retry Logic
Implement exponential backoff for failed jobs

### Scale to Cloud
Move to AWS Lambda + SQS or Google Cloud Functions + Pub/Sub
