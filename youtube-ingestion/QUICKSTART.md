# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd youtube-ingestion
pip install -r requirements.txt
```

### 2. Get YouTube API Key
- Go to: https://console.cloud.google.com/
- Create project → Enable YouTube Data API v3 → Create API Key
- Copy the key

### 3. Create .env File
```bash
cp .env.example .env
```

Edit `.env`:
```
YOUTUBE_API_KEY=YOUR_API_KEY_HERE
OUTPUT_FOLDER=./transcripts
```

### 4. Add Your Channels
Edit `config.py`, find the `CHANNELS` list, and add your Jain channels:

```python
CHANNELS: List[ChannelConfig] = [
    ChannelConfig(
        name="Your Channel Name",
        channel_id="UCxxxxxxxxxxxxxx",
        description="Description"
    ),
]
```

To find channel ID: Visit the YouTube channel, it's in the URL as `/channel/CHANNEL_ID`

### 5. Start the Pipeline
```bash
python scheduler.py
```

✓ Done! The pipeline will now:
- Check your channels at 6 AM & 6 PM IST
- Download transcripts automatically
- Save them to `./transcripts`

## Check Status

While the pipeline is running, in another terminal:

```bash
# View statistics
python cli.py stats

# List recent jobs
python cli.py jobs

# Get job details
python cli.py job-detail <job_id>
```

## Manual Testing

Before running the full scheduler, test individual components:

```bash
# Test monitoring (check for new videos)
python monitor_agent.py

# Test processing (download transcripts)
python process_agent.py

# View configuration
python cli.py config
```

## Troubleshooting

### API Key Error
- Check `.env` file exists with `YOUTUBE_API_KEY`
- Verify the key is valid at https://console.cloud.google.com/

### No Videos Found
- Verify channel IDs are correct
- Check channels have uploaded videos recently
- Check monitoring logs: `tail -f ingestion.log`

### Transcript Download Failed
- Some videos don't have transcripts on YouTube
- Check YouTube directly to confirm
- Pipeline will retry automatically

## Next: Integration

Once working, you can:

1. **Integrate with doc-transcribe API**
   - POST downloaded transcripts to the API
   - Trigger additional NLP processing

2. **Add Notifications**
   - Email when new transcripts are ready
   - Webhook to Slack/Discord

3. **Scale to Cloud**
   - Deploy to AWS Lambda or Google Cloud Functions
   - Use managed services instead of local database

See README.md for full documentation.
