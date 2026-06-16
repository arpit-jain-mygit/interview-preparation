import logging
import os
import json
from pathlib import Path
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

from config import Config
from database import Database, JobStatus

logger = logging.getLogger(__name__)

class ProcessAgent:
    """Agent that processes pending jobs and downloads transcripts."""

    def __init__(self):
        self.db = Database()
        self._setup_output_folder()

    def _setup_output_folder(self):
        """Ensure output folder exists."""
        Path(Config.OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output folder ready: {Config.OUTPUT_FOLDER}")

    def process_pending_jobs(self, limit: int = 10) -> int:
        """Process pending jobs. Returns count of successfully processed jobs."""
        jobs = self.db.get_pending_jobs(limit)

        if not jobs:
            logger.info("No pending jobs to process")
            return 0

        processed_count = 0
        for job in jobs:
            try:
                success = self._process_job(job)
                if success:
                    processed_count += 1
            except Exception as e:
                logger.error(f"Error processing job {job['job_id']}: {str(e)}")
                self.db.update_job_status(
                    job['job_id'],
                    JobStatus.FAILED,
                    error=str(e)
                )

        return processed_count

    def _process_job(self, job: dict) -> bool:
        """Process a single job: download transcript and save it."""
        job_id = job['job_id']
        video_id = job['video_id']
        channel_id = job['channel_id']

        # Mark job as processing
        self.db.update_job_status(job_id, JobStatus.PROCESSING)
        logger.info(f"Processing job {job_id} (video: {video_id})")

        try:
            # Download transcript
            transcript = self._download_transcript(video_id)
            if not transcript:
                raise Exception("Failed to download transcript")

            # Save transcript to file
            transcript_path = self._save_transcript(video_id, channel_id, transcript)

            # Mark job as completed
            self.db.update_job_status(job_id, JobStatus.COMPLETED, transcript_path=transcript_path)
            logger.info(f"Job {job_id} completed. Transcript saved to: {transcript_path}")
            return True

        except Exception as e:
            logger.error(f"Job {job_id} failed: {str(e)}")
            self.db.update_job_status(job_id, JobStatus.FAILED, error=str(e))
            return False

    def _download_transcript(self, video_id: str) -> Optional[list]:
        """Download transcript for a video."""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            logger.info(f"Downloaded transcript for video {video_id}: {len(transcript)} entries")
            return transcript
        except TranscriptsDisabled:
            logger.warning(f"Transcripts are disabled for video {video_id}")
            raise Exception("Transcripts disabled")
        except NoTranscriptFound:
            logger.warning(f"No transcript found for video {video_id}")
            raise Exception("No transcript available")
        except Exception as e:
            logger.error(f"Error downloading transcript for {video_id}: {str(e)}")
            raise

    def _save_transcript(self, video_id: str, channel_id: str, transcript: list) -> str:
        """Save transcript to file. Returns the path."""
        # Create channel-specific subdirectory
        channel_folder = Path(Config.OUTPUT_FOLDER) / channel_id
        channel_folder.mkdir(parents=True, exist_ok=True)

        # Save as JSON and plain text
        transcript_filename = f"{video_id}.json"
        transcript_path = channel_folder / transcript_filename

        # Convert transcript entries to readable format
        full_text = "\n".join([entry["text"] for entry in transcript])

        # Save JSON
        with open(transcript_path, "w", encoding="utf-8") as f:
            json.dump({
                "video_id": video_id,
                "channel_id": channel_id,
                "transcript": transcript,
                "full_text": full_text
            }, f, ensure_ascii=False, indent=2)

        # Save plain text
        text_path = channel_folder / f"{video_id}.txt"
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        logger.info(f"Saved transcript to {transcript_path}")
        return str(transcript_path)

    def run(self, limit: int = 10):
        """Run the process agent."""
        logger.info("Starting transcript processing...")
        processed = self.process_pending_jobs(limit)
        logger.info(f"Processing cycle complete. {processed} job(s) processed successfully.")
        return processed


if __name__ == "__main__":
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    agent = ProcessAgent()
    agent.run()
