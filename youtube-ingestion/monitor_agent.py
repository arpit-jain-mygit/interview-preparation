import logging
from datetime import datetime
from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import Config, ChannelConfig
from database import Database, JobStatus

logger = logging.getLogger(__name__)

class MonitorAgent:
    """Agent that monitors YouTube channels for new videos."""

    def __init__(self):
        if not Config.YOUTUBE_API_KEY:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set")
        self.youtube = build("youtube", "v3", developerKey=Config.YOUTUBE_API_KEY)
        self.db = Database()

    def monitor_channels(self) -> int:
        """Monitor all configured channels for new videos. Returns count of new videos found."""
        total_new_videos = 0

        for channel in Config.CHANNELS:
            try:
                new_count = self._check_channel(channel)
                total_new_videos += new_count
                self.db.log_channel_check(channel.channel_id, new_count, "success")
                logger.info(f"Channel '{channel.name}': Found {new_count} new videos")
            except Exception as e:
                logger.error(f"Error monitoring channel '{channel.name}': {str(e)}")
                self.db.log_channel_check(channel.channel_id, 0, f"error: {str(e)}")

        return total_new_videos

    def _check_channel(self, channel: ChannelConfig) -> int:
        """Check a single channel for new videos."""
        new_videos_count = 0

        try:
            # Get the channel's uploads playlist
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel.channel_id
            )
            response = request.execute()

            if not response.get("items"):
                logger.warning(f"Channel {channel.channel_id} not found")
                return 0

            uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

            # Get recent videos from the uploads playlist
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,  # Check last 50 videos
                order="date"
            )
            response = request.execute()

            for item in response.get("items", []):
                video_id = item["snippet"]["resourceId"]["videoId"]
                title = item["snippet"]["title"]
                published_at = item["snippet"]["publishedAt"]

                # Try to record the video (returns True if new)
                is_new = self.db.record_video(video_id, channel.channel_id, title, published_at)

                if is_new:
                    # Create a processing job for this new video
                    job_id = self.db.create_job(video_id, channel.channel_id)
                    logger.info(f"New video found: {title} (video_id: {video_id}, job_id: {job_id})")
                    new_videos_count += 1

            return new_videos_count

        except HttpError as e:
            logger.error(f"YouTube API error: {str(e)}")
            raise

    def run(self):
        """Run the monitor agent."""
        logger.info("Starting channel monitoring...")
        new_videos = self.monitor_channels()
        logger.info(f"Monitor cycle complete. {new_videos} new video(s) found.")
        return new_videos


if __name__ == "__main__":
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    agent = MonitorAgent()
    agent.run()
