#!/usr/bin/env python3
"""Command-line interface for managing the YouTube transcript ingestion pipeline."""

import logging
import click
from tabulate import tabulate
import sqlite3
from datetime import datetime

from config import Config
from database import Database, JobStatus
from monitor_agent import MonitorAgent
from process_agent import ProcessAgent
from scheduler import Scheduler

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@click.group()
def cli():
    """YouTube Transcript Ingestion Pipeline CLI."""
    pass

@cli.command()
def monitor():
    """Run the monitor agent to check for new videos."""
    click.echo("Starting monitor agent...")
    agent = MonitorAgent()
    new_count = agent.run()
    click.echo(f"✓ Monitor cycle complete. Found {new_count} new video(s).")

@cli.command()
@click.option('--limit', default=10, help='Maximum jobs to process')
def process(limit):
    """Run the process agent to download transcripts."""
    click.echo("Starting process agent...")
    agent = ProcessAgent()
    processed = agent.run(limit)
    click.echo(f"✓ Processing cycle complete. Processed {processed} job(s).")

@cli.command()
def start():
    """Start the full scheduler (continuous mode)."""
    click.echo("Starting ingestion pipeline scheduler...")
    click.echo("Press Ctrl+C to stop")
    scheduler = Scheduler()
    scheduler.start()
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("\nStopping scheduler...")
        scheduler.stop()
        click.echo("✓ Scheduler stopped.")

@cli.command()
def jobs():
    """List all processing jobs."""
    db = Database()
    try:
        with sqlite3.connect(db.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT job_id, video_id, channel_id, status, created_at FROM jobs ORDER BY created_at DESC LIMIT 20")
            rows = cursor.fetchall()

        if not rows:
            click.echo("No jobs found.")
            return

        table_data = []
        for row in rows:
            table_data.append([
                row['job_id'][:8] + '...',
                row['video_id'],
                row['channel_id'][:12] + '...',
                row['status'],
                row['created_at'][:19]
            ])

        headers = ['Job ID', 'Video ID', 'Channel ID', 'Status', 'Created']
        click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.option('--status', type=click.Choice(['pending', 'processing', 'completed', 'failed']), help='Filter by status')
def stats(status):
    """Show pipeline statistics."""
    db = Database()
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()

            # Total videos
            cursor.execute("SELECT COUNT(*) FROM videos")
            total_videos = cursor.fetchone()[0]

            # Jobs by status
            cursor.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
            job_stats = dict(cursor.fetchall())

            click.echo("\n📊 Pipeline Statistics")
            click.echo("=" * 40)
            click.echo(f"Total Videos Found: {total_videos}")
            click.echo("\nJobs by Status:")
            for s in ['pending', 'processing', 'completed', 'failed']:
                count = job_stats.get(s, 0)
                click.echo(f"  {s.capitalize()}: {count}")

            # Recent monitoring checks
            cursor.execute("""
                SELECT channel_id, check_time, videos_found, status
                FROM monitoring_log
                ORDER BY check_time DESC
                LIMIT 10
            """)
            recent = cursor.fetchall()

            if recent:
                click.echo("\nRecent Monitoring Checks:")
                table_data = []
                for row in recent:
                    table_data.append([
                        row[0][:12] + '...',
                        row[1][:19],
                        row[2],
                        row[3]
                    ])
                headers = ['Channel ID', 'Check Time', 'Videos Found', 'Status']
                click.echo(tabulate(table_data, headers=headers, tablefmt='simple'))

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
@click.argument('job_id')
def job_detail(job_id):
    """Show details for a specific job."""
    db = Database()
    job = db.get_job_by_id(job_id)

    if not job:
        click.echo(f"Job {job_id} not found.", err=True)
        return

    click.echo(f"\n📋 Job Details")
    click.echo("=" * 50)
    click.echo(f"Job ID:          {job['job_id']}")
    click.echo(f"Video ID:        {job['video_id']}")
    click.echo(f"Channel ID:      {job['channel_id']}")
    click.echo(f"Status:          {job['status']}")
    click.echo(f"Created:         {job['created_at']}")
    click.echo(f"Updated:         {job['updated_at']}")
    if job['transcript_path']:
        click.echo(f"Transcript Path: {job['transcript_path']}")
    if job['error_message']:
        click.echo(f"Error:           {job['error_message']}")

@cli.command()
def config():
    """Show current configuration."""
    click.echo("\n⚙️  Configuration")
    click.echo("=" * 50)
    click.echo(f"YouTube API Key: {'Set' if Config.YOUTUBE_API_KEY else 'NOT SET ⚠️'}")
    click.echo(f"Database Path:   {Config.DB_PATH}")
    click.echo(f"Output Folder:   {Config.OUTPUT_FOLDER}")
    click.echo(f"Morning Check:   {Config.MORNING_CHECK_TIME} IST")
    click.echo(f"Evening Check:   {Config.EVENING_CHECK_TIME} IST")
    click.echo(f"Max Retries:     {Config.MAX_RETRIES}")
    click.echo(f"\nChannels to Monitor: {len(Config.CHANNELS)}")
    for ch in Config.CHANNELS:
        click.echo(f"  • {ch.name} ({ch.channel_id})")

if __name__ == '__main__':
    cli()
