import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from config import Config

class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Database:
    """SQLite-based job queue for managing video processing."""

    def __init__(self, db_path: str = Config.DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Videos table - records of videos found on YouTube
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    video_id TEXT PRIMARY KEY,
                    channel_id TEXT NOT NULL,
                    title TEXT,
                    published_at TIMESTAMP,
                    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Jobs table - processing jobs for transcripts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    video_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    transcript_path TEXT,
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id)
                )
            """)

            # Monitoring log - tracks when channels were last checked
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monitoring_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT NOT NULL,
                    check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    videos_found INTEGER DEFAULT 0,
                    status TEXT
                )
            """)

            conn.commit()

    def record_video(self, video_id: str, channel_id: str, title: str, published_at: str) -> bool:
        """Record a new video if it doesn't exist. Returns True if new, False if duplicate."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO videos (video_id, channel_id, title, published_at) VALUES (?, ?, ?, ?)",
                    (video_id, channel_id, title, published_at)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False  # Video already exists

    def create_job(self, video_id: str, channel_id: str) -> str:
        """Create a processing job for a video. Returns job_id."""
        import uuid
        job_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO jobs (job_id, video_id, channel_id, status)
                   VALUES (?, ?, ?, ?)""",
                (job_id, video_id, channel_id, JobStatus.PENDING.value)
            )
            conn.commit()
        return job_id

    def get_pending_jobs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get pending jobs for processing."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM jobs WHERE status = ? LIMIT ?""",
                (JobStatus.PENDING.value, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

    def update_job_status(self, job_id: str, status: JobStatus, transcript_path: Optional[str] = None, error: Optional[str] = None):
        """Update job status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE jobs SET status = ?, transcript_path = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE job_id = ?""",
                (status.value, transcript_path, error, job_id)
            )
            conn.commit()

    def log_channel_check(self, channel_id: str, videos_found: int, status: str = "success"):
        """Log a channel monitoring check."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO monitoring_log (channel_id, videos_found, status)
                   VALUES (?, ?, ?)""",
                (channel_id, videos_found, status)
            )
            conn.commit()

    def get_job_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific job by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
