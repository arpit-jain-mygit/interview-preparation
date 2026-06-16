# Setup Checklist

Complete these steps to get your pipeline running:

## Prerequisites
- [ ] Python 3.8+ installed
- [ ] pip package manager available
- [ ] Internet connection to YouTube API
- [ ] Google Cloud Console account (free)

## 1. YouTube API Setup
- [ ] Go to https://console.cloud.google.com/
- [ ] Create a new project (or select existing)
- [ ] Search for "YouTube Data API v3"
- [ ] Click "Enable"
- [ ] Go to "Credentials"
- [ ] Create "API Key" credential type
- [ ] Copy the API key (keep it secret!)

## 2. Local Environment Setup
- [ ] Navigate to `youtube-ingestion` directory
  ```bash
  cd youtube-ingestion
  ```
- [ ] Create Python virtual environment (optional but recommended)
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```
- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

## 3. Configuration
- [ ] Copy `.env.example` to `.env`
  ```bash
  cp .env.example .env
  ```
- [ ] Edit `.env` and add your YouTube API key
  ```
  YOUTUBE_API_KEY=your_api_key_here
  ```

## 4. Add Your Channels
- [ ] Open `config.py` in a text editor
- [ ] Find the `CHANNELS` list (around line 17)
- [ ] For each Jain channel you want to monitor:
  - [ ] Visit the YouTube channel URL
  - [ ] Copy the channel ID from URL (`/channel/UCxxxxx`)
  - [ ] Add entry to CHANNELS list:
    ```python
    ChannelConfig(
        name="Channel Name",
        channel_id="UCxxxxxxxxxxxxxx",
        description="Description"
    )
    ```

## 5. Test Individual Components
- [ ] Test monitor agent:
  ```bash
  python monitor_agent.py
  ```
  - Should list any videos found on your channels
  - Check logs for "New video found" messages
  
- [ ] Test process agent:
  ```bash
  python process_agent.py
  ```
  - Should process any pending jobs
  - Check `transcripts/` folder for downloaded files

- [ ] View configuration:
  ```bash
  python cli.py config
  ```
  - Verify your channels are listed
  - Verify API key is recognized

- [ ] View statistics:
  ```bash
  python cli.py stats
  ```
  - Should show pipeline state

## 6. Start the Full Pipeline
- [ ] Run the scheduler:
  ```bash
  python scheduler.py
  ```
- [ ] Should see:
  - "Scheduler started successfully"
  - Morning/evening times logged
  - Processing interval logged
  
- [ ] Monitor progress:
  - In another terminal:
    ```bash
    python cli.py stats
    python cli.py jobs
    ```
  - Watch `ingestion.log` for activity:
    ```bash
    tail -f ingestion.log
    ```

## 7. Verify Output
- [ ] Check transcripts folder:
  ```bash
  ls -R transcripts/
  ```
- [ ] Should contain:
  - Subdirectories for each channel (by channel_id)
  - `.json` and `.txt` files for each transcript

## 8. Keep Running
- [ ] Stop with Ctrl+C, or let it run in background:
  
  **Option A: nohup (Simple)**
  ```bash
  nohup python scheduler.py > ingestion.log 2>&1 &
  ```
  
  **Option B: tmux (Better)**
  ```bash
  tmux new-session -d -s ingestion "python scheduler.py"
  tmux attach -t ingestion  # To view
  tmux kill-session -t ingestion  # To stop
  ```
  
  **Option C: Docker (Recommended)**
  ```bash
  docker-compose up -d
  docker-compose logs -f
  ```

## 9. Optional: Add More Channels Later
- [ ] Edit `config.py` and add more channels to the list
- [ ] Restart the pipeline (Ctrl+C, then `python scheduler.py`)
- [ ] New channels will be checked on next monitoring cycle

## Troubleshooting During Setup

### "YOUTUBE_API_KEY is not set"
- [ ] Verify `.env` file exists
- [ ] Verify `YOUTUBE_API_KEY=...` is in `.env`
- [ ] Restart terminal/Python process

### "No module named 'googleapiclient'"
- [ ] Run `pip install -r requirements.txt` again
- [ ] Verify you're in the correct virtual environment

### "Channel not found"
- [ ] Verify channel ID is correct (should be `UCxxxxxx` format)
- [ ] Channel might be private or deleted
- [ ] Check the exact URL at the channel

### "No transcript found"
- [ ] Some videos on YouTube don't have transcripts
- [ ] Check the video directly on YouTube
- [ ] Pipeline will skip and continue with other videos

### "ModuleNotFoundError: No module named 'dotenv'"
- [ ] Ensure `.env` file exists (for python-dotenv)
- [ ] Or manually set environment variables:
  ```bash
  export YOUTUBE_API_KEY=your_key
  python scheduler.py
  ```

## What's Next?

After successful setup:

1. **Monitor the pipeline** - Check `stats` and `jobs` regularly
2. **Integrate with doc-transcribe** - POST transcripts to your API
3. **Add more channels** - Edit config.py and restart
4. **Scale to cloud** - See DEPLOYMENT.md for AWS/GCP options
5. **Add notifications** - Email/Slack when transcripts are ready

## Getting Help

- Check logs: `tail -f ingestion.log`
- View config: `python cli.py config`
- View jobs: `python cli.py jobs`
- See README.md for full documentation
