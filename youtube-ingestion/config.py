import os
from typing import List
from dataclasses import dataclass
from datetime import time

@dataclass
class ChannelConfig:
    """Configuration for a YouTube channel to monitor."""
    name: str
    channel_id: str
    description: str = ""

class Config:
    """Application configuration."""

    # YouTube API
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

    # Channels to monitor (Jain channels)
    CHANNELS: List[ChannelConfig] = [
        ChannelConfig(
            name="Channel 1",
            channel_id="UCxxxxxxxxxxxxxx",
            description="Jain Channel 1"
        ),
        # Add more channels as needed
    ]

    # Schedule times (IST - India Standard Time)
    MORNING_CHECK_TIME = time(6, 0)  # 6 AM IST
    EVENING_CHECK_TIME = time(18, 0)  # 6 PM IST

    # Database
    DB_PATH = os.getenv("DB_PATH", "transcripts.db")

    # Output folder for downloaded transcripts
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "./transcripts")

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "ingestion.log"
